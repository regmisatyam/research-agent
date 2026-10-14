#!/usr/bin/env python3
"""
Additional analysis: deepcopy overhead impact on sorted_builtin timing.
"""
import copy
import time
import random

# Measure deepcopy overhead for different sizes
sizes = [100, 1000, 3000]
rng = random.Random(42)

for size in sizes:
    data = [rng.randint(-100000, 100000) for _ in range(size)]
    
    # Time deepcopy
    times = []
    for _ in range(1000):
        start = time.perf_counter_ns()
        copy.deepcopy(data)
        end = time.perf_counter_ns()
        times.append(end - start)
    
    mean_dc = sum(times) / len(times)
    print(f"deepcopy n={size}: mean={mean_dc:,.0f} ns")

print()

# Now check: for sorted_builtin at n=100, the total time is ~950 ns
# If deepcopy takes ~X ns, then the actual sort takes ~950-X ns
# This means the reported "sorted_builtin" time is inflated by deepcopy overhead

# Measure sorted_builtin actual time (without deepcopy)
data = [rng.randint(-100000, 100000) for _ in range(100)]
times = []
for _ in range(1000):
    start = time.perf_counter_ns()
    sorted(data)
    end = time.perf_counter_ns()
    times.append(end - start)
mean_sorted = sum(times) / len(times)
print(f"sorted() n=100 (no deepcopy): mean={mean_sorted:,.0f} ns")

# The report measures: deepcopy + sorted()
# So the actual sort time is: report_mean - deepcopy_mean
print()
print("Interpretation:")
print("The benchmark measures: deepcopy(data) + sorted(timed_data)")
print("For n=100 random: report mean = 950 ns")
print("If deepcopy takes ~500 ns, actual sort takes ~450 ns")
print("This means ~50% of the measured time is deepcopy overhead.")
print()

# Check all sorted_builtin configs
print("sorted_builtin timing breakdown estimate:")
for size in sizes:
    data = [rng.randint(-100000, 100000) for _ in range(size)]
    dc_times = []
    for _ in range(500):
        start = time.perf_counter_ns()
        copy.deepcopy(data)
        end = time.perf_counter_ns()
        dc_times.append(end - start)
    mean_dc = sum(dc_times) / len(dc_times)
    
    sort_times = []
    for _ in range(500):
        start = time.perf_counter_ns()
        sorted(data)
        end = time.perf_counter_ns()
        sort_times.append(end - start)
    mean_sort = sum(sort_times) / len(sort_times)
    
    print(f"  n={size}: deepcopy={mean_dc:,.0f} ns, sorted={mean_sort:,.0f} ns, ratio={mean_dc/(mean_dc+mean_sort)*100:.0f}% of total")
