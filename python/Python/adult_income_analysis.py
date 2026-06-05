import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =====================
# 1. Load Dataset
# =====================
df = pd.read_csv('/mnt/data/AssignmentCompletePandas.ipynb', low_memory=False)

# =====================
# 2. Basic Overview
# =====================
print("\n1. Shape (Rows, Columns):", df.shape)
print("\n2. Data Types:\n", df.dtypes)
print("\n3. Unique Values per Column:\n", df.nunique())
print("\n4. Target Distribution (Income):\n", df['income'].value_counts(normalize=True) * 100)

# =====================
# 3. Summary Statistics
# =====================
numeric_cols = df.select_dtypes(include=[np.number])
print("\n5. Summary Statistics:\n", numeric_cols.describe())

# =====================
# 4. Age Distribution
# =====================
plt.figure(figsize=(8, 4))
sns.histplot(df['age'], bins=30, kde=True)
plt.title('6. Age Distribution')
plt.xlabel('Age')
plt.show()

# =====================
# 5. Hours-per-Week Distribution
# =====================
plt.figure(figsize=(8, 4))
sns.histplot(df['hours-per-week'], bins=30, kde=False)
plt.title('7. Hours per Week Distribution')
plt.xlabel('Hours per Week')
plt.show()

print("\nExtreme values:")
print(df[df['hours-per-week'].isin([0, 99, 100])])

# =====================
# 6. Highest Capital Gain/Loss
# =====================
print("\n8. Highest Capital Gain:\n", df[df['capital-gain'] == df['capital-gain'].max()])
print("\nHighest Capital Loss:\n", df[df['capital-loss'] == df['capital-loss'].max()])

# =====================
# 7. Workclass Analysis
# =====================
print("\n10. Workclass counts:\n", df['workclass'].value_counts())
sns.countplot(y='workclass', data=df, order=df['workclass'].value_counts().index)
plt.title('Workclass Distribution')
plt.show()

# =====================
# 8. Education Analysis
# =====================
print("\n11. Education counts:\n", df['education'].value_counts())
print("\n12. Educational-num mapping check:")
print(df[['education', 'educational-num']].drop_duplicates().sort_values('educational-num'))

sns.countplot(y='education', data=df, order=df['education'].value_counts().index)
plt.title('Education Distribution')
plt.show()

# =====================
# 9. Occupation, Marital Status, Race, Gender
# =====================
print("\n13. Occupations:\n", df['occupation'].value_counts())
sns.countplot(y='occupation', data=df, order=df['occupation'].value_counts().index)
plt.title('Occupation Distribution')
plt.show()

print("\n14. Marital Status:\n", df['marital-status'].value_counts())
sns.countplot(y='marital-status', data=df, order=df['marital-status'].value_counts().index)
plt.title('Marital Status Distribution')
plt.show()

print("\n15. Gender Distribution:\n", df['gender'].value_counts(normalize=True) * 100)
sns.countplot(x='gender', data=df)
plt.title('Gender Distribution')
plt.show()

print("\n16. Race Distribution:\n", df['race'].value_counts())
sns.countplot(y='race', data=df, order=df['race'].value_counts().index)
plt.title('Race Distribution')
plt.show()

print("\n17. Native Country counts:\n", df['native-country'].value_counts().head(10))

# =====================
# 10. Relationships Between Features
# =====================
# 18. Income vs Education
edu_income_percent = pd.crosstab(df['education'], df['income'], normalize='index') * 100
ax = edu_income_percent.plot(kind='bar', stacked=True, figsize=(12, 6), color=["#69b3a2", "#d95f02"])
plt.title('Income Distribution by Education Level')
plt.xlabel('Education Level')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=45)
for container in ax.containers:
    ax.bar_label(container, fmt="%.1f%%", label_type="center", fontsize=8, color="white")
plt.tight_layout()
plt.show()

# 19. Age vs Income
plt.figure(figsize=(8, 4))
sns.boxplot(x='income', y='age', data=df)
plt.title('Age vs Income')
plt.show()

# 20. Occupation vs Income
plt.figure(figsize=(10, 5))
occupation_income = pd.crosstab(df['occupation'], df['income'], normalize='index') * 100
occupation_income.sort_values(by='>50K', inplace=True)
occupation_income.plot(kind='barh', stacked=True, figsize=(10, 6))
plt.title('Occupation vs Income')
plt.show()

# 21. Gender vs Income
sns.countplot(x='gender', hue='income', data=df)
plt.title('Gender vs Income')
plt.show()

# 22. Race vs Income
race_income = pd.crosstab(df['race'], df['income'], normalize='index') * 100
race_income.plot(kind='bar', stacked=True)
plt.title('Race vs Income')
plt.show()

# 23. Hours-per-Week vs Income
plt.figure(figsize=(8, 4))
sns.boxplot(x='income', y='hours-per-week', data=df)
plt.title('Hours-per-Week vs Income')
plt.show()

# 24. Capital-gain Influence
plt.figure(figsize=(8, 4))
sns.boxplot(x='income', y='capital-gain', data=df)
plt.ylim(0, 50000)
plt.title('Capital-Gain vs Income')
plt.show()

# =====================
# 11. Additional Tasks 25-36 (Summary, Outliers, Top Categories)
# =====================
print("\n25. Total Observations & Features:", df.shape)
print("\n26. Data Types (again):\n", df.dtypes)
print("\n27. Target Distribution:\n", df['income'].value_counts(normalize=True) * 100)
print("\n28. Min, Max, Mean, Median:\n", numeric_cols.agg(['min','max','mean','median']))

# 29. Outlier detection using IQR
for col in ['age','hours-per-week','capital-gain','capital-loss']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))]
    print(f"Outliers in {col}: {len(outliers)}")

# 30. Top 5 categories per categorical column
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"\nTop 5 {col} categories:\n", df[col].value_counts().head())

# 31. Unique countries count
print("\n31. Unique Native Countries:", df['native-country'].nunique())

# 32. Education vs Income Relationship (already plotted)

# 33. Average Age per Income Group
print("\n33. Average Age per Income Group:\n", df.groupby('income')['age'].mean())

# 34. Hours-per-Week Distribution by Income
sns.kdeplot(data=df, x='hours-per-week', hue='income', fill=True)
plt.title('Hours-per-Week by Income')
plt.show()

# 35. Occupation with Highest Proportion >50K
occ_income = pd.crosstab(df['occupation'], df['income'], normalize='index')
print("\n35. Occupation Proportion >50K:\n", occ_income.sort_values(by='>50K', ascending=False).head())

# 36. Gender Distribution across Workclass
sns.countplot(x='workclass', hue='gender', data=df)
plt.xticks(rotation=45)
plt.title('Gender Distribution across Workclass')
plt.show()
