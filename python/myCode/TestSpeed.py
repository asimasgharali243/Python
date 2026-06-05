import numpy as np
import time

# Number of elements for comparison
N = 1_000_00  # 100k elements (adjust if your system is slow)

print(f"Comparing performance for {N} elements...\n")

# ------------------------------
# 1. CREATION SPEED
# ------------------------------
start = time.time()
py_list = [i for i in range(N)]
end = time.time()
print(f"Python List Creation Time: {end - start:.6f} sec")

start = time.time()
np_array = np.arange(N)
end = time.time()
print(f"NumPy Array Creation Time: {end - start:.6f} sec\n")

# ------------------------------
# 2. ELEMENT-WISE OPERATION SPEED
# (e.g., adding 5 to each element)
# ------------------------------
start = time.time()
py_list_result = [x + 5 for x in py_list]
end = time.time()
print(f"Python List Operation Time: {end - start:.6f} sec")

start = time.time()
np_result = np_array + 5
end = time.time()
print(f"NumPy Array Operation Time: {end - start:.6f} sec\n")

# ------------------------------
# 3. ACCESS SPEED (Random Access)
# ------------------------------
index = N // 2
start = time.time()
_ = py_list[index]
end = time.time()
print(f"Python List Access Time: {end - start:.10f} sec")

start = time.time()
_ = np_array[index]
end = time.time()
print(f"NumPy Array Access Time: {end - start:.10f} sec\n")

# ------------------------------
# 4. APPEND & DELETION SPEED
# ------------------------------
# Append
start = time.time()
py_list.append(999)
end = time.time()
print(f"Python List Append Time: {end - start:.10f} sec")

start = time.time()
np_array = np.append(np_array, 999)
end = time.time()
print(f"NumPy Array Append Time: {end - start:.10f} sec (copies entire array!)\n")

# Deletion
start = time.time()
del py_list[-1]
end = time.time()
print(f"Python List Deletion Time: {end - start:.10f} sec")

start = time.time()
np_array = np.delete(np_array, -1)
end = time.time()
print(f"NumPy Array Deletion Time: {end - start:.10f} sec (slow - creates new array!)\n")

print("✅ Comparison completed!")
