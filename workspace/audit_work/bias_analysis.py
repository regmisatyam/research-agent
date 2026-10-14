#!/usr/bin/env python3
"""
Check: Does the benchmark design introduce bias between algorithms?

The benchmark does:
  timed_data = copy.deepcopy(data)  # NOT timed
  start = time.perf_counter_ns()
  algo_fn(timed_data)               # timed
  end = time.perf_counter_ns()

For insertion_sort: a = list(arr) is done INSIDE the timed section
For merge_sort: a = list(arr) is done INSIDE the timed section
For sorted_builtin: sorted() creates a new list INSIDE the timed section

So:
- insertion_sort timed = list(arr) + sort in-place
- merge_sort timed = list(arr) + recursive sort
- sorted_builtin timed = sorted() (creates new list internally)

The list(arr) copy for insertion_sort and merge_sort is an EXTRA copy
beyond the deepcopy that was already done. This adds overhead to the
timed section for these algorithms but not for sorted_builtin.

This is a methodological inconsistency.
"""
import copy
import time
import random

# Measure the overhead
rng = random.Random(42)
data = [rng.randint(-100000, 100000) for _ in range(100)]

# Scenario 1: deepcopy before timing, then list(arr) inside timing (like insertion_sort)
times1 = []
for _ in range(1000):
    timed_data = copy.deepcopy(data)
    start = time.perf_counter_ns()
    a = list(timed_data)  # extra copy
    end = time.perf_counter_ns()
    times1.append(end - start)
print(f"deepcopy + list(arr): mean={sum(times1)/len(times1):,.0f} ns")

# Scenario 2: deepcopy before timing, then sorted() inside timing (like sorted_builtin)
times2 = []
for _ in range(1000):
    timed_data = copy.deepcopy(data)
    start = time.perf_counter_ns()
    sorted(timed_data)
    end = time.perf_counter_ns()
    times2.append(end - start)
print(f"deepcopy + sorted(): mean={sum(times2)/len(times2):,.0f} ns")

# Scenario 3: no deepcopy, just list(arr) inside timing (what insertion_sort would be without deepcopy)
times3 = []
for _ in range(1000):
    start = time.perf_counter_ns()
    a = list(data)
    end = time.perf_counter_ns()
    times3.append(end - start)
print(f"list(arr) only: mean={sum(times3)/len(times3):,.0f} ns")

# Scenario 4: no deepcopy, just sorted() inside timing
times4 = []
for _ in range(1000):
    start = time.perf_counter_ns()
    sorted(data)
    end = time.perf_counter_ns()
    times4.append(end - start)
print(f"sorted() only: mean={sum(times4)/len(times4):,.0f} ns")

print()
print("Analysis:")
print(f"  deepcopy overhead: {sum(times1)/len(times1) - sum(times3)/len(times3):,.0f} ns")
print(f"  sorted() overhead: {sum(times2)/len(times2) - sum(times4)/len(times4):,.0f} ns")
print()
print(f"  The deepcopy before timing adds ~{sum(times1)/len(times1) - sum(times3)/len(times3):,.0f} ns")
print(f"  to insertion_sort/merge_sort timed measurements but NOT to sorted_builtin.")
print(f"  This makes insertion_sort/merge_sort appear slower by ~{sum(times1)/len(times1) - sum(times3)/len(times3):,.0f} ns.")
print()
print(f"  For n=100, this is ~{sum(times1)/len(times1) - sum(times3)/len(times3):,.0f} ns out of ~{sum(times1)/len(times1):,.0f} ns")
print(f"  total, or ~{(sum(times1)/len(times1) - sum(times3)/len(times3)) / (sum(times1)/len(times1)) * 100:.0f}% of the measurement.")
