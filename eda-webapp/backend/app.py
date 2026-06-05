import os, io, uuid, base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import IsolationForest
from scipy import stats
from sklearn.preprocessing import PowerTransformer
from scipy.stats import boxcox
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)

# -------------------- Helper Functions --------------------

def save_df_to_csv(df, file_id):
    path = os.path.join(PROCESSED_FOLDER, f"{file_id}.csv")
    df.to_csv(path, index=False)
    return path

def load_df(file_id):
    p1 = os.path.join(PROCESSED_FOLDER, f"{file_id}.csv")
    p2 = os.path.join(UPLOAD_FOLDER, f"{file_id}.csv")
    if os.path.exists(p1):
        return pd.read_csv(p1)
    elif os.path.exists(p2):
        return pd.read_csv(p2)
    else:
        raise FileNotFoundError("File not found")

def df_to_base64_plot(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

def add_index_column(df):
    """Return a DataFrame preview including an explicit index column."""
    df_reset = df.reset_index().rename(columns={"index": "Index"})
    return df_reset.to_dict(orient="records")

# -------------------- Upload --------------------

@app.route("/api/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "no file uploaded"}), 400
    
    file_id = str(uuid.uuid4())
    fname = f.filename.lower()
    ext = os.path.splitext(fname)[1]
    save_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.csv")

    try:
        if ext == ".csv":
            f.save(save_path)
        else:
            df = pd.read_excel(f)
            df.to_csv(save_path, index=False)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    df = pd.read_csv(save_path)
    return jsonify({
        "file_id": file_id,
        "preview": add_index_column(df.head(5)),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "shape": df.shape
    })

# -------------------- Preview --------------------

@app.route("/api/preview/<file_id>", methods=["GET"])
def preview(file_id):
    df = load_df(file_id)
    n = int(request.args.get("n", 5))
    return jsonify({
        "preview": add_index_column(df.head(n)),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "shape": df.shape
    })

# -------------------- Data Types Overview --------------------

@app.route("/api/dtypes/<file_id>", methods=["GET"])
def get_dtypes(file_id):
    """Return all column names with their data types."""
    df = load_df(file_id)
    dtypes = df.dtypes.astype(str).to_dict()
    return jsonify({
        "columns": list(df.columns),
        "dtypes": dtypes,
        "preview": add_index_column(df.head(5))
    })


# -------------------- Change Data Type --------------------

@app.route("/api/change_dtype/<file_id>", methods=["POST"])
def change_dtype(file_id):
    payload = request.get_json() or {}
    column = payload.get("column")
    new_type = payload.get("new_type")

    if not column or not new_type:
        return jsonify({"error": "Column and new_type required"}), 400

    df = load_df(file_id)

    if column not in df.columns:
        return jsonify({"error": f"Column '{column}' not found"}), 404

    # Conversion logic
    try:
        if new_type == "int":
            df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")
        elif new_type == "float":
            df[column] = pd.to_numeric(df[column], errors="coerce").astype(float)
        elif new_type == "string":
            df[column] = df[column].astype(str)
        elif new_type == "category":
            df[column] = df[column].astype("category")
        elif new_type == "datetime":
            df[column] = pd.to_datetime(df[column], errors="coerce")
        else:
            return jsonify({"error": f"Unsupported type '{new_type}'"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to convert: {str(e)}"}), 500

    save_df_to_csv(df, file_id)

    return jsonify({
        "message": f"Column '{column}' converted to {new_type}.",
        "dtypes": df.dtypes.astype(str).to_dict(),
        "preview": add_index_column(df.head(5))
    })




# -------------------- Summary --------------------

@app.route("/api/summary/<file_id>", methods=["GET"])
def summary(file_id):
    df = load_df(file_id)
    total_rows = len(df)
    missing = df.isnull().sum().to_dict()
    missing_pct = (df.isnull().mean() * 100).round(2).to_dict()
    num = df.select_dtypes(include=[np.number])
    num_stats = num.describe().to_dict()
    cat_stats = {}
    for c in df.select_dtypes(include=['object','category']).columns:
        vc = df[c].value_counts(dropna=False).head(10)
        cat_stats[c] = vc.to_dict()
    return jsonify({
        "shape": df.shape,
        "missing": missing,
        "missing_pct": missing_pct,
        "numeric_stats": num_stats,
        "categorical_top_values": cat_stats
    })

# -------------------- Missing Analysis --------------------

@app.route("/api/missing_analysis/<file_id>", methods=["GET"])
def missing_analysis(file_id):
    df = load_df(file_id)
    missing_counts = df.isnull().sum()
    missing_pct = (df.isnull().mean() * 100).round(2)
    data = [
        {"column": col, "nullCount": int(missing_counts[col]), "nullPct": float(missing_pct[col])}
        for col in df.columns
    ]

    plt.switch_backend("Agg")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="coolwarm", ax=ax)
    plt.title("Missing Values Heatmap", fontsize=14)
    img = df_to_base64_plot(fig)
    
    return jsonify({
        "missing_data": data,
        "total_missing": int(missing_counts.sum()),
        "heatmap": img
    })

# -------------------- Imputation --------------------

@app.route("/api/impute/<file_id>", methods=["POST"])
def impute(file_id):
    payload = request.get_json() or {}
    column = payload.get("column")
    method = payload.get("method", "mean")

    df = load_df(file_id)
    df_new = df.copy()

    if column not in df.columns:
        return jsonify({"error": f"Column '{column}' not found"}), 400

    # Numeric Columns
    if df[column].dtype in [np.float64, np.int64]:
        if method == "mean":
            imp = SimpleImputer(strategy="mean")
        elif method == "median":
            imp = SimpleImputer(strategy="median")
        elif method == "knn":
            imp = KNNImputer(n_neighbors=5)
        elif method == "iterative":
            imp = IterativeImputer()
        elif method == "constant":
            fill_value = payload.get("fill_value", 0)
            imp = SimpleImputer(strategy="constant", fill_value=fill_value)
        else:
            return jsonify({"error": f"Unknown method '{method}'"}), 400
        df_new[[column]] = imp.fit_transform(df_new[[column]])
    else:
        # Categorical Columns
        if method == "mode":
            mode_val = df_new[column].mode().iloc[0] if not df_new[column].mode().empty else "missing"
            df_new[column] = df_new[column].fillna(mode_val)
        elif method == "constant":
            fill_value = payload.get("fill_value", "missing")
            df_new[column] = df_new[column].fillna(fill_value)
        else:
            return jsonify({"error": f"Unknown method '{method}' for categorical"}), 400

    save_df_to_csv(df_new, file_id)

    return jsonify({
        "message": f"Missing values in column '{column}' filled using {method}.",
        "missing_after": int(df_new[column].isnull().sum()),
        "preview": add_index_column(df_new.head(5))
    })

# -------------------- Duplicate Check --------------------

@app.route("/api/duplicates/<file_id>", methods=["GET"])
def check_duplicates(file_id):
    df = load_df(file_id)
    duplicates = df[df.duplicated()]
    count = len(duplicates)

    return jsonify({
        "duplicate_count": count,
        "has_duplicates": count > 0,
        "preview": add_index_column(duplicates.head(10)) if count > 0 else [],
        "total_rows": len(df),
        "percent": round((count / len(df)) * 100, 2) if len(df) > 0 else 0
    })

# -------------------- Remove Duplicates --------------------

@app.route("/api/remove_duplicates/<file_id>", methods=["POST"])
def remove_duplicates(file_id):
    payload = request.get_json() or {}
    method = payload.get("method", "keep_first")

    df = load_df(file_id)

    if method == "keep_first":
        df_cleaned = df.drop_duplicates(keep="first")
    elif method == "keep_last":
        df_cleaned = df.drop_duplicates(keep="last")
    elif method == "remove_all":
        df_cleaned = df[~df.duplicated(keep=False)]
    else:
        return jsonify({"error": f"Unknown method '{method}'"}), 400

    save_df_to_csv(df_cleaned, file_id)

    return jsonify({
        "message": f"Duplicates handled using method '{method}'.",
        "rows_before": len(df),
        "rows_after": len(df_cleaned),
        "duplicates_removed": len(df) - len(df_cleaned),
        "preview": add_index_column(df_cleaned.head(5))
    })




# ---------------- OUTLIER ANALYSIS ------------------

@app.route("/api/outlier_analysis/<file_id>", methods=["GET"])
def outlier_analysis(file_id):
    df = load_df(file_id)
    num_df = df.select_dtypes(include=[np.number])

    if num_df.empty:
        return jsonify({"error": "No numeric columns found."}), 400

    outlier_summary = []
    plt.switch_backend("Agg")

    # Outlier detection summary
    for col in num_df.columns:
        q1, q3 = num_df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        iqr_outliers = num_df[(num_df[col] < lower) | (num_df[col] > upper)][col].count()

        z_scores = np.abs(stats.zscore(num_df[col].dropna()))
        z_outliers = np.sum(z_scores > 3)

        outlier_summary.append({
            "column": col,
            "iqr_outliers": int(iqr_outliers),
            "z_outliers": int(z_outliers),
            "total": int(max(iqr_outliers, z_outliers)),
        })

    # Generate combined boxplot for all numeric columns
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=num_df, orient="h", ax=ax)
    plt.title("Boxplot for Outlier Visualization", fontsize=14)
    plt.tight_layout()
    boxplot_img = df_to_base64_plot(fig)

    # Histogram for overall outlier effect
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.histplot(num_df.melt()["value"], bins=30, kde=True, ax=ax2)
    plt.title("Distribution Overview", fontsize=13)
    plt.tight_layout()
    hist_img = df_to_base64_plot(fig2)

    return jsonify({
        "outlier_summary": outlier_summary,
        "boxplot": boxplot_img,
        "histogram": hist_img
    })


# ---------------- REMOVE OUTLIERS ------------------

@app.route("/api/remove_outliers/<file_id>", methods=["POST"])
def remove_outliers(file_id):
    payload = request.get_json() or {}
    method = payload.get("method", "iqr")
    columns = payload.get("columns", [])

    df = load_df(file_id)
    num_df = df.select_dtypes(include=[np.number])

    if not columns:
        columns = num_df.columns.tolist()

    df_new = df.copy()

    for col in columns:
        if col not in num_df.columns:
            continue

        if method == "iqr":
            q1, q3 = df_new[col].quantile([0.25, 0.75])
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            df_new = df_new[(df_new[col] >= lower) & (df_new[col] <= upper)]

        elif method == "zscore":
            z_scores = np.abs(stats.zscore(df_new[col].dropna()))
            mask = (z_scores < 3)
            df_new = df_new.loc[df_new[col].dropna().index[mask]]

        elif method == "percentile":
            lower = df_new[col].quantile(0.01)
            upper = df_new[col].quantile(0.99)
            df_new = df_new[(df_new[col] >= lower) & (df_new[col] <= upper)]

        elif method == "isolation_forest":
            iso = IsolationForest(contamination=0.05, random_state=42)
            mask = iso.fit_predict(df_new[[col]].fillna(0))
            df_new = df_new[mask == 1]

        else:
            return jsonify({"error": f"Unknown method: {method}"}), 400

    save_df_to_csv(df_new, file_id)

    # Return before-after summary
    return jsonify({
        "message": f"Outliers removed using {method}.",
        "shape_before": df.shape,
        "shape_after": df_new.shape,
        "preview": df_new.head(5).to_dict(orient="records")
    })

# -------------------- Transformations (Standardize / Normalize / Log / etc.) --------------------
from scipy.stats import boxcox
from sklearn.preprocessing import PowerTransformer

@app.route("/api/transform_options/<file_id>", methods=["GET"])
def transform_options(file_id):
    """Return numeric columns available for transformation and basic stats."""
    df = load_df(file_id)
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    stats = {}
    for c in num_cols:
        series = df[c].dropna()
        stats[c] = {
            "count": int(series.count()),
            "mean": float(series.mean()) if not series.empty else None,
            "std": float(series.std()) if not series.empty else None,
            "min": float(series.min()) if not series.empty else None,
            "max": float(series.max()) if not series.empty else None,
        }
    return jsonify({"numeric_columns": num_cols, "stats": stats})


def plot_before_after(df, columns, title_prefix=""):
    """Create combined histogram + boxplot image for given columns and return base64."""
    plt.switch_backend("Agg")
    # Combined figure with two rows: histograms (top) and boxplots (bottom)
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), gridspec_kw={"height_ratios": [3, 1]})
    # Top: histogram(s) using melted values for better overlay
    melted = df[columns].melt(value_name="value", var_name="column")
    sns.histplot(data=melted, x="value", hue="column", element="step", stat="density", common_norm=False, ax=axes[0], alpha=0.6)
    axes[0].set_title(f"{title_prefix} Distribution (histograms)")
    # Bottom: boxplot
    sns.boxplot(data=df[columns], orient="h", ax=axes[1])
    axes[1].set_title(f"{title_prefix} Boxplots")
    plt.tight_layout()
    return df_to_base64_plot(fig)


@app.route("/api/transform/<file_id>", methods=["POST"])
def transform_columns(file_id):
    """
    Apply transformation to specified columns.
    JSON payload:
    {
      "columns": ["col1","col2"],        # optional; if omitted, apply to all numeric cols
      "method": "standardize" | "normalize" | "log" | "sqrt" | "boxcox" | "minmax" | "robust" | "yeo-johnson",
      "clip_negative_for_log": true      # optional, default False (will coerce negatives to NaN for log/boxcox)
    }
    """
    payload = request.get_json() or {}
    method = payload.get("method", "standardize")
    columns = payload.get("columns", [])
    clip_neg = payload.get("clip_negative_for_log", False)

    df = load_df(file_id)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        return jsonify({"error": "No numeric columns found for transformation."}), 400

    # determine target columns
    if not columns:
        columns = numeric_cols
    else:
        # sanitize to only numeric columns that exist
        columns = [c for c in columns if c in numeric_cols]
        if not columns:
            return jsonify({"error": "No valid numeric columns specified."}), 400

    # produce before image using current data (only selected cols)
    before_img = plot_before_after(df, columns, title_prefix="Before")

    df_new = df.copy()

    # Apply transformations column-wise
    for col in columns:
        s = df_new[col].copy()
        try:
            if method in ["standardize", "zscore"]:
                # mean 0, std 1
                df_new[col] = (s - s.mean()) / s.std()
            elif method in ["normalize", "minmax"]:
                denom = (s.max() - s.min())
                if denom == 0 or pd.isna(denom):
                    df_new[col] = 0
                else:
                    df_new[col] = (s - s.min()) / denom
            elif method == "log":
                # use log1p for stability; handle negatives if requested
                if clip_neg:
                    s = s.clip(lower=0)
                df_new[col] = np.log1p(s)
            elif method == "sqrt":
                s = s.clip(lower=0)
                df_new[col] = np.sqrt(s)
            elif method == "boxcox":
                # boxcox requires strictly positive data. fallback to yeo-johnson via PowerTransformer if negative present
                arr = s.dropna().values
                if (arr <= 0).any():
                    # fallback
                    pt = PowerTransformer(method="yeo-johnson")
                    transformed = pt.fit_transform(s.values.reshape(-1, 1)).flatten()
                    df_new[col] = pd.Series(transformed, index=s.index)
                else:
                    # safe to apply boxcox for non-negative strictly positive values
                    # apply boxcox to non-null portion and assign back
                    transformed, _ = boxcox(arr)
                    df_new.loc[s.dropna().index, col] = transformed
            elif method in ["yeo-johnson", "power"]:
                pt = PowerTransformer(method="yeo-johnson")
                transformed = pt.fit_transform(s.values.reshape(-1, 1)).flatten()
                df_new[col] = pd.Series(transformed, index=s.index)
            elif method == "robust":
                # subtract median and divide by IQR (robust scaling)
                med = s.median()
                iqr = s.quantile(0.75) - s.quantile(0.25)
                if pd.isna(iqr) or iqr == 0:
                    df_new[col] = s - med
                else:
                    df_new[col] = (s - med) / iqr
            else:
                return jsonify({"error": f"Unknown transformation method '{method}'"}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to transform column '{col}': {str(e)}"}), 500

    # produce after image for same columns
    after_img = plot_before_after(df_new, columns, title_prefix="After")

    # save transformed dataframe
    save_df_to_csv(df_new, file_id)

    return jsonify({
        "message": f"Applied '{method}' transformation on columns: {columns}",
        "before_img": before_img,
        "after_img": after_img,
        "preview": add_index_column(df_new.head(5)),
        "dtypes": df_new.dtypes.astype(str).to_dict()
    })


# -------------------- Categorical Labeling / Encoding --------------------

@app.route("/api/label_options/<file_id>", methods=["GET"])
def label_options(file_id):
    """
    Return categorical columns detected automatically via select_dtypes.
    """
    try:
        df = load_df(file_id)
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        return jsonify({"categorical_columns": cat_cols})
    except FileNotFoundError:
        return jsonify({"error": "file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def _series_bar_plot_base64(series, title=""):
    """Create simple bar plot for a Series.value_counts() and return base64 PNG."""
    plt.switch_backend("Agg")
    fig, ax = plt.subplots(figsize=(6, 3))
    # Make sure we don't try to plot empty series
    if series.dropna().empty:
        ax.text(0.5, 0.5, "No data", ha="center", va="center")
    else:
        vc = series.value_counts(dropna=False)
        ax.bar(vc.index.astype(str), vc.values, edgecolor="black")
        ax.set_xticklabels([str(x) for x in vc.index], rotation=45, ha="right", fontsize=8)
    ax.set_title(title)
    plt.tight_layout()
    return df_to_base64_plot(fig)


@app.route("/api/label_encode/<file_id>", methods=["POST"])
def label_encode(file_id):
    """
    Apply encoding on a categorical column.
    Payload JSON:
    {
      "column": "colName",
      "method": "label" | "onehot" | "custom",
      "mapping": {"catA": 1, "catB": 0}   # required for custom
    }
    Returns: before_img, after_img, preview (with Index), dtypes, message, mapping (for label/custom)
    """
    payload = request.get_json() or {}
    column = payload.get("column")
    method = payload.get("method", "label")
    mapping = payload.get("mapping", {})

    if not column:
        return jsonify({"error": "column required"}), 400

    try:
        df = load_df(file_id)
    except FileNotFoundError:
        return jsonify({"error": "file not found"}), 404

    if column not in df.columns:
        return jsonify({"error": f"Column '{column}' not found"}), 400

    # ensure column is categorical-ish
    if df[column].dtype not in [object, "category"] and not pd.api.types.is_string_dtype(df[column]):
        # We'll still allow encoding but warn—convert to string first
        df[column] = df[column].astype(str)

    # BEFORE plot
    before_img = _series_bar_plot_base64(df[column], title=f"Before: {column}")

    result_mapping = None

    try:
        if method == "label":
            # convert to categorical and get codes; keep mapping to return
            cat = df[column].astype("category")
            codes = cat.cat.codes  # -1 for NaN
            categories = list(cat.cat.categories)
            # build mapping: category -> code
            result_mapping = {str(cat_val): int(i) for i, cat_val in enumerate(categories)}
            # apply codes (NaN will be -1; we map NaN to None)
            df[column] = cat.cat.codes.replace({-1: None}).astype("Int64")

        elif method == "onehot":
            # create dummies and drop original column
            dummies = pd.get_dummies(df[column], prefix=column, dummy_na=False)
            df = pd.concat([df.drop(columns=[column]), dummies], axis=1)

        elif method == "custom":
            if not mapping or not isinstance(mapping, dict):
                return jsonify({"error": "custom method requires 'mapping' dict in payload"}), 400
            # apply mapping; keep values unmapped as they are
            df[column] = df[column].map(lambda v: mapping.get(str(v), mapping.get(v, v)))
            # build mapping to return (string keys)
            result_mapping = {str(k): v for k, v in mapping.items()}

        else:
            return jsonify({"error": f"Unknown method '{method}'"}), 400

        # AFTER plot: for onehot we can plot sums of dummy columns (first 10 if many)
        if method == "onehot":
            dummy_cols = [c for c in df.columns if c.startswith(f"{column}_")]
            if not dummy_cols:
                after_img = _series_bar_plot_base64(pd.Series([]), title=f"After One-Hot: {column}")
            else:
                # sum each dummy to show counts per category
                sums = df[dummy_cols].sum().sort_values(ascending=False)
                # convert to series for plotting
                after_img = _series_bar_plot_base64(sums, title=f"After One-Hot counts ({column})")
        else:
            after_img = _series_bar_plot_base64(df[column], title=f"After: {column}")

        # Save transformed dataframe (to processed folder)
        save_df_to_csv(df, file_id)

        preview = add_index_column(df.head(10))
        dtypes = df.dtypes.astype(str).to_dict()

        response = {
            "message": f"{method} encoding applied on {column}",
            "before_img": before_img,
            "after_img": after_img,
            "preview": preview,
            "dtypes": dtypes
        }
        if result_mapping is not None:
            response["mapping"] = result_mapping

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# -------------------- COLUMN SELECTION FOR TRAINING --------------------

@app.route("/api/column_selection/<file_id>", methods=["GET"])
def column_selection(file_id):
    """
    Return all available columns with data types to let user choose
    training and target columns.
    """
    try:
        df = load_df(file_id)
        columns = df.columns.tolist()
        dtypes = df.dtypes.astype(str).to_dict()
        return jsonify({
            "columns": columns,
            "dtypes": dtypes,
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=["object", "category"]).columns.tolist()
        })
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/select_columns/<file_id>", methods=["POST"])
def select_columns(file_id):
    """
    Accepts:
    {
      "train_columns": ["col1", "col2", ...],
      "target_column": "colY"
    }
    Ensures target column is not in train columns.
    """
    payload = request.get_json() or {}
    train_columns = payload.get("train_columns", [])
    target_column = payload.get("target_column")

    try:
        df = load_df(file_id)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

    all_columns = df.columns.tolist()

    # Validation
    if not target_column:
        return jsonify({"error": "Target column is required"}), 400
    if target_column not in all_columns:
        return jsonify({"error": f"Target column '{target_column}' not found"}), 400

    invalid_train_cols = [c for c in train_columns if c not in all_columns]
    if invalid_train_cols:
        return jsonify({"error": f"Invalid training columns: {invalid_train_cols}"}), 400

    if target_column in train_columns:
        return jsonify({"error": "Target column cannot be included in training columns"}), 400

    # Everything is valid
    selection_info = {
        "file_id": file_id,
        "train_columns": train_columns,
        "target_column": target_column,
        "train_shape": df[train_columns].shape if train_columns else None,
        "target_dtype": str(df[target_column].dtype)
    }

    # Save selection for later use (optional)
    sel_path = os.path.join(PROCESSED_FOLDER, f"{file_id}_selection.json")
    import json
    with open(sel_path, "w") as f:
        json.dump(selection_info, f, indent=2)

    return jsonify({
        "message": "Training and target columns selected successfully.",
        "selection": selection_info
    })

@app.route("/api/train_model/<file_id>", methods=["POST"])
def train_model(file_id):
    """
    Payload:
    {
      "model": "linear" | "ridge" | "lasso" | "decision_tree" | "random_forest" | "logistic"
    }
    """
    payload = request.get_json() or {}
    model_name = payload.get("model", "linear")

    # Load column selection
    sel_path = os.path.join(PROCESSED_FOLDER, f"{file_id}_selection.json")
    if not os.path.exists(sel_path):
        return jsonify({"error": "Column selection not found"}), 400
    import json
    with open(sel_path) as f:
        selection = json.load(f)

    train_cols = selection.get("train_columns", [])
    target_col = selection.get("target_column")
    df = load_df(file_id)

    if not train_cols or not target_col:
        return jsonify({"error": "Train or target columns not set"}), 400

    # Prepare data
    X = df[train_cols].values
    y = df[target_col].values

    is_classification = model_name == "logistic"

    # Instantiate model
    try:
        if model_name == "linear":
            model = LinearRegression()
        elif model_name == "ridge":
            model = Ridge()
        elif model_name == "lasso":
            model = Lasso()
        elif model_name == "decision_tree":
            model = DecisionTreeClassifier() if is_classification else DecisionTreeRegressor()
        elif model_name == "random_forest":
            model = RandomForestClassifier(n_estimators=100, random_state=42) if is_classification else RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_name == "logistic":
            model = LogisticRegression(max_iter=500)
            if df[target_col].dtype not in [np.int64, np.int32]:
                df[target_col] = pd.factorize(df[target_col])[0]
                y = df[target_col].values
        else:
            return jsonify({"error": f"Unknown model '{model_name}'"}), 400

        # Train
        model.fit(X, y)
        if is_classification:
            y_pred = model.predict(X)
            score = accuracy_score(y, y_pred)
            score_type = "accuracy"
        else:
            score = model.score(X, y)
            score_type = "r2_score"

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "message": f"{model_name} model trained successfully.",
        "score": round(score, 4),
        "score_type": score_type,
        "train_columns": train_cols,
        "target_column": target_col
    })


# -------------------- Run App --------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
