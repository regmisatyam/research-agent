#!/usr/bin/env python3
"""
Sorting algorithm benchmark: insertion sort, merge sort, and Python's sorted().

Research question: How do input size and input order affect running time?

Uses only Python standard library.
"""

import copy
import csv
import os
import random
import statistics
import sys
import time


# ---------------------------------------------------------------------------
# Algorithms
# ---------------------------------------------------------------------------

def insertion_sort(arr):
    """In-place insertion sort. Returns the sorted list."""
    a = list(arr)  # work on a copy
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    """Top-down merge sort. Returns a new sorted list."""
    a = list(arr)  # work on a copy
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return _merge(left, right)


def _merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# Correctness tests
# ---------------------------------------------------------------------------

def run_correctness_tests():
    """Verify each algorithm against sorted() on edge cases."""
    algorithms = {
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "sorted_builtin": sorted,
    }

    test_cases = {
        "empty": [],
        "single": [42],
        "two_elements": [3, 1],
        "two_equal": [5, 5],
        "duplicates": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        "negatives": [-5, -1, -3, -2, -4],
        "mixed_neg_pos": [-10, 3, 0, -7, 2, 1],
        "already_sorted": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "reverse_sorted": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "all_same": [7, 7, 7, 7, 7],
        "large_random": list(range(1000)) + list(range(1000)),
    }

    print("=" * 60)
    print("CORRECTNESS TESTS")
    print("=" * 60)

    all_passed = True
    for name, algo_fn in algorithms.items():
        print(f"\n{name}:")
        for tc_name, data in test_cases.items():
            expected = sorted(data)
            result = algo_fn(data)
            passed = result == expected
            if not passed:
                all_passed = False
                print(f"  FAIL  {tc_name}: got {result[:20]}... expected {expected[:20]}...")
            else:
                print(f"  PASS  {tc_name}")

    print()
    if all_passed:
        print("All correctness tests PASSED.")
    else:
        print("SOME correctness tests FAILED.")
    print()
    return all_passed


# ---------------------------------------------------------------------------
# Benchmark helpers
# ---------------------------------------------------------------------------

def generate_input(size, input_type, seed):
    """Generate a list of integers for benchmarking."""
    rng = random.Random(seed)
    if input_type == "random":
        return [rng.randint(-100000, 100000) for _ in range(size)]
    elif input_type == "sorted":
        # Generate random sorted data
        data = [rng.randint(-100000, 100000) for _ in range(size)]
        data.sort()
        return data
    elif input_type == "reverse_sorted":
        data = [rng.randint(-100000, 100000) for _ in range(size)]
        data.sort(reverse=True)
        return data
    else:
        raise ValueError(f"Unknown input_type: {input_type}")


def benchmark_one(algo_name, algo_fn, data, warmup_runs=10, repeat=50):
    """
    Benchmark a single algorithm on a single input.
    Returns (mean_elapsed_ns, all_elapsed_ns_list, correct_bool).
    """
    # Warm-up runs (not timed)
    warm_data = copy.deepcopy(data)
    for _ in range(warmup_runs):
        algo_fn(warm_data)

    # Correctness check (on a copy)
    correct = algo_fn(list(data)) == sorted(data)

    # Timed runs
    elapsed_ns = []
    for _ in range(repeat):
        timed_data = copy.deepcopy(data)  # fresh copy each repetition
        start = time.perf_counter_ns()
        algo_fn(timed_data)
        end = time.perf_counter_ns()
        elapsed_ns.append(end - start)

    mean_ns = statistics.mean(elapsed_ns)
    return mean_ns, elapsed_ns, correct


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_experiment():
    """Run the full benchmark experiment and save results."""
    sizes = [100, 1000, 3000]
    input_types = ["random", "sorted", "reverse_sorted"]
    seeds = [42, 123, 456, 789, 1000]
    repetitions = 50
    warmup_runs = 10

    algorithms = {
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "sorted_builtin": sorted,
    }

    results = []
    total_configs = len(sizes) * len(input_types) * len(seeds) * len(algorithms) * repetitions
    print(f"Total measurements to collect: {total_configs}")
    print()

    config_count = 0
    for size in sizes:
        for input_type in input_types:
            for seed in seeds:
                # Generate input ONCE
                base_data = generate_input(size, input_type, seed)

                for algo_name, algo_fn in algorithms.items():
                    config_count += 1
                    print(
                        f"[{config_count}/{total_configs}] "
                        f"size={size}, type={input_type}, seed={seed}, algo={algo_name}"
                    )

                    mean_ns, all_ns, correct = benchmark_one(
                        algo_name, algo_fn, base_data,
                        warmup_runs=warmup_runs, repeat=repetitions
                    )

                    for i, elapsed in enumerate(all_ns):
                        results.append({
                            "algorithm": algo_name,
                            "size": size,
                            "input_type": input_type,
                            "seed": seed,
                            "repetition": i + 1,
                            "elapsed_ns": elapsed,
                            "correct": correct,
                        })

    # Save to CSV
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.csv")
    fieldnames = [
        "algorithm", "size", "input_type", "seed",
        "repetition", "elapsed_ns", "correct",
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print()
    print(f"Results saved to {csv_path}")
    print(f"Total rows: {len(results)}")

    # Quick summary
    print()
    print("=" * 60)
    print("SUMMARY (mean elapsed_ns)")
    print("=" * 60)
    summary = {}
    for r in results:
        key = (r["algorithm"], r["size"], r["input_type"])
        if key not in summary:
            summary[key] = []
        summary[key].append(r["elapsed_ns"])

    for key in sorted(summary.keys()):
        algo, size, itype = key
        vals = summary[key]
        mean_val = statistics.mean(vals)
        std_val = statistics.stdev(vals) if len(vals) > 1 else 0
        print(f"  {algo:20s}  size={size:5d}  {itype:15s}  mean={mean_val:>12.0f} ns  std={std_val:>10.0f} ns")

    return results


if __name__ == "__main__":
    # Step 1: Correctness
    ok = run_correctness_tests()
    if not ok:
        print("Correctness tests failed. Aborting benchmark.")
        sys.exit(1)

    # Step 2: Benchmark
    run_experiment()
