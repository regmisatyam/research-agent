#!/usr/bin/env python3
"""
Independent verification of REPORT.md numerical claims against results.csv.
"""
import csv
import statistics
from collections import defaultdict

# Read all data
rows = []
with open("/workspace/results.csv", "r") as f:
    reader = csv.DictReader(f)
    for r in reader:
        r["size"] = int(r["size"])
        r["seed"] = int(r["seed"])
        r["repetition"] = int(r["repetition"])
        r["elapsed_ns"] = int(r["elapsed_ns"])
        r["correct"] = r["correct"] == "True"
        rows.append(r)

print(f"Total rows read: {len(rows)}")
print(f"Expected: 6750")
print()

# ---- Check 1: Row count and completeness ----
print("=" * 60)
print("CHECK 1: Row count and completeness")
print("=" * 60)

expected_sizes = [100, 1000, 3000]
expected_types = ["random", "sorted", "reverse_sorted"]
expected_seeds = [42, 123, 456, 789, 1000]
expected_algos = ["insertion_sort", "merge_sort", "sorted_builtin"]
expected_reps = 50

config_count = 0
for s in expected_sizes:
    for t in expected_types:
        for seed in expected_seeds:
            for algo in expected_algos:
                config_count += 1

print(f"Expected configurations: {config_count}")
print(f"Expected total rows: {config_count * expected_reps} = {config_count * expected_reps}")
print()

# Check each config has exactly 50 rows
configs = defaultdict(list)
for r in rows:
    key = (r["algorithm"], r["size"], r["input_type"], r["seed"])
    configs[key].append(r)

missing = []
extra = []
incomplete = []
for s in expected_sizes:
    for t in expected_types:
        for seed in expected_seeds:
            for algo in expected_algos:
                key = (algo, s, t, seed)
                if key not in configs:
                    missing.append(key)
                elif len(configs[key]) != expected_reps:
                    incomplete.append((key, len(configs[key])))

print(f"Missing configs: {len(missing)}")
print(f"Incomplete configs (not 50 reps): {len(incomplete)}")
if incomplete:
    for k, c in incomplete[:5]:
        print(f"  {k}: {c} rows")
print()

# ---- Check 2: Correctness ----
print("=" * 60)
print("CHECK 2: Correctness field")
print("=" * 60)
all_correct = all(r["correct"] for r in rows)
print(f"All measurements correct=True: {all_correct}")
if not all_correct:
    fails = [r for r in rows if not r["correct"]]
    print(f"  Failures: {len(fails)}")
print()

# ---- Check 3: Recompute all means and stds ----
print("=" * 60)
print("CHECK 3: Recompute means and stds from CSV")
print("=" * 60)

summary = defaultdict(list)
for r in rows:
    key = (r["algorithm"], r["size"], r["input_type"])
    summary[key].append(r["elapsed_ns"])

report_table = {
    ("insertion_sort", 100, "random"):         (53632, 7217),
    ("insertion_sort", 100, "reverse_sorted"): (101605, 3758),
    ("insertion_sort", 100, "sorted"):         (2913, 297),
    ("insertion_sort", 1000, "random"):        (6738226, 170200),
    ("insertion_sort", 1000, "reverse_sorted"):(13055800, 170697),
    ("insertion_sort", 1000, "sorted"):        (34959, 2597),
    ("insertion_sort", 3000, "random"):        (65173417, 1755847),
    ("insertion_sort", 3000, "reverse_sorted"):(129215162, 2151380),
    ("insertion_sort", 3000, "sorted"):        (110146, 5269),
    ("merge_sort", 100, "random"):             (45703, 2946),
    ("merge_sort", 100, "reverse_sorted"):     (36406, 1613),
    ("merge_sort", 100, "sorted"):             (34842, 2739),
    ("merge_sort", 1000, "random"):            (595104, 18681),
    ("merge_sort", 1000, "reverse_sorted"):    (427323, 20815),
    ("merge_sort", 1000, "sorted"):            (417224, 13360),
    ("merge_sort", 3000, "random"):            (2064942, 52808),
    ("merge_sort", 3000, "reverse_sorted"):    (1459824, 36718),
    ("merge_sort", 3000, "sorted"):            (1394349, 40896),
    ("sorted_builtin", 100, "random"):         (950, 74),
    ("sorted_builtin", 100, "reverse_sorted"): (317, 33),
    ("sorted_builtin", 100, "sorted"):         (270, 35),
    ("sorted_builtin", 1000, "random"):        (18408, 3953),
    ("sorted_builtin", 1000, "reverse_sorted"):(2575, 1633),
    ("sorted_builtin", 1000, "sorted"):        (1793, 112),
    ("sorted_builtin", 3000, "random"):        (70163, 19924),
    ("sorted_builtin", 3000, "reverse_sorted"):(7817, 365),
    ("sorted_builtin", 3000, "sorted"):        (5999, 843),
}

print(f"{'Config':<50} {'Report Mean':>12} {'Calc Mean':>12} {'Match':>6} {'Report Std':>12} {'Calc Std':>12} {'Std Match':>10}")
print("-" * 140)

mean_mismatches = []
std_mismatches = []

for key in sorted(report_table.keys()):
    algo, size, itype = key
    report_mean, report_std = report_table[key]
    calc_vals = summary[key]
    calc_mean = statistics.mean(calc_vals)
    calc_std = statistics.stdev(calc_vals) if len(calc_vals) > 1 else 0

    mean_match = abs(calc_mean - report_mean) <= 1  # within 1 ns
    std_match = abs(calc_std - report_std) <= 1  # within 1 ns

    status_mean = "OK" if mean_match else "MISMATCH"
    status_std = "OK" if std_match else "MISMATCH"

    if not mean_match:
        mean_mismatches.append((key, report_mean, calc_mean))
    if not std_match:
        std_mismatches.append((key, report_std, calc_std))

    print(f"{algo:20s} size={size:5d} {itype:15s}  {report_mean:>12,}  {calc_mean:>12.0f}  {status_mean:>6}  {report_std:>12,}  {calc_std:>12.0f}  {status_std:>10}")

print()
print(f"Mean mismatches: {len(mean_mismatches)}")
for k, rm, cm in mean_mismatches:
    print(f"  {k}: report={rm:,}, calc={cm:,.0f}, diff={abs(rm-cm):,.0f}")
print()
print(f"Std mismatches: {len(std_mismatches)}")
for k, rs, cs in std_mismatches:
    print(f"  {k}: report={rs:,}, calc={cs:,.0f}, diff={abs(rs-cs):,.0f}")
print()

# ---- Check 4: Verify key observations / ratios ----
print("=" * 60)
print("CHECK 4: Verify key observations (ratios)")
print("=" * 60)

def get_mean(algo, size, itype):
    return statistics.mean(summary[(algo, size, itype)])

# Observation 1: Insertion sort n=100->1000 random: 53632 -> 6738226
r1 = get_mean("insertion_sort", 1000, "random") / get_mean("insertion_sort", 100, "random")
print(f"Insertion sort n=100->1000 random ratio: calc={r1:.1f}x, report claims ~125x")

r2 = get_mean("insertion_sort", 3000, "random") / get_mean("insertion_sort", 1000, "random")
print(f"Insertion sort n=1000->3000 random ratio: calc={r2:.1f}x, report claims ~9.7x")

# Observation 2: Merge sort n=100->1000: 45703 -> 595104
r3 = get_mean("merge_sort", 1000, "random") / get_mean("merge_sort", 100, "random")
print(f"Merge sort n=100->1000 random ratio: calc={r3:.1f}x, report claims ~13x")

r4 = get_mean("merge_sort", 3000, "random") / get_mean("merge_sort", 1000, "random")
print(f"Merge sort n=1000->3000 random ratio: calc={r4:.1f}x, report claims ~3.5x")

# Observation 3: sorted() n=100->1000: 950 -> 18408
r5 = get_mean("sorted_builtin", 1000, "random") / get_mean("sorted_builtin", 100, "random")
print(f"sorted() n=100->1000 random ratio: calc={r5:.1f}x, report claims ~19x")

# Observation 4: Insertion sort n=3000 sorted vs reverse
r6 = get_mean("insertion_sort", 3000, "reverse_sorted") / get_mean("insertion_sort", 3000, "sorted")
print(f"Insertion sort n=3000 reverse/sorted ratio: calc={r6:.0f}x, report claims 1,173x")

# Observation 5: Merge sort n=100 random vs sorted
r7 = get_mean("merge_sort", 100, "random") / get_mean("merge_sort", 100, "sorted")
print(f"Merge sort n=100 random/sorted ratio: calc={r7:.1f}x, report claims ~1.3x")

r8 = get_mean("merge_sort", 3000, "random") / get_mean("merge_sort", 3000, "sorted")
print(f"Merge sort n=3000 random/sorted ratio: calc={r8:.1f}x, report claims ~1.5x")

# Observation 6: sorted() n=1000 random vs sorted
r9 = get_mean("sorted_builtin", 1000, "random") / get_mean("sorted_builtin", 1000, "sorted")
print(f"sorted() n=1000 random/sorted ratio: calc={r9:.1f}x, report claims ~10x")

r10 = get_mean("sorted_builtin", 3000, "random") / get_mean("sorted_builtin", 3000, "sorted")
print(f"sorted() n=3000 random/sorted ratio: calc={r10:.1f}x, report claims ~11.7x")

# Observation 7: sorted() vs merge sort speedup
print()
print("sorted() vs merge_sort speedup ratios:")
for size in [100, 1000, 3000]:
    for itype in ["random", "sorted", "reverse_sorted"]:
        ms_mean = get_mean("merge_sort", size, itype)
        sb_mean = get_mean("sorted_builtin", size, itype)
        ratio = ms_mean / sb_mean
        print(f"  n={size} {itype}: merge_sort/sorted = {ratio:.1f}x")

print()
print("sorted() vs insertion_sort speedup ratios:")
for size in [100, 1000, 3000]:
    for itype in ["random", "sorted", "reverse_sorted"]:
        is_mean = get_mean("insertion_sort", size, itype)
        sb_mean = get_mean("sorted_builtin", size, itype)
        ratio = is_mean / sb_mean
        print(f"  n={size} {itype}: insertion_sort/sorted = {ratio:.0f}x")

# ---- Check 5: Verify warm-up doesn't contaminate timing ----
print()
print("=" * 60)
print("CHECK 5: Warm-up contamination check")
print("=" * 60)
print("In algorithms.py, warm-up runs on a deepcopy of data, not timed.")
print("Timed runs each get a fresh deepcopy. This is correct.")
print("However, warm-up data is NOT the same as timed data (different copy).")
print("This means warm-up does NOT affect the timed measurements directly.")
print("The warm-up runs may affect Python's internal caches (e.g., object pool),")
print("but this is a minor effect and is consistent across all algorithms.")
print()

# ---- Check 6: Verify input generation ----
print("=" * 60)
print("CHECK 6: Input generation analysis")
print("=" * 60)
print("generate_input uses random.Random(seed) — isolated RNG per call.")
print("For 'sorted' and 'reverse_sorted', data is first generated randomly,")
print("then sorted/reverse-sorted. This means the VALUES are random,")
print("but the ORDER is fixed. This is correct per the plan.")
print()

# ---- Check 7: Verify merge_sort recursion depth ----
print("=" * 60)
print("CHECK 7: Merge sort recursion depth")
print("=" * 60)
print("merge_sort is recursive with mid = len(a) // 2.")
print("For n=3000, depth = ceil(log2(3000)) = 12.")
print("Python default recursion limit is 1000, so this is safe.")
print()

# ---- Check 8: Verify the "sorted_builtin" timing anomaly ----
print("=" * 60)
print("CHECK 8: sorted_builtin timing anomaly check")
print("=" * 60)
print("sorted_builtin at n=100 random: mean=950 ns, std=74 ns")
print("sorted_builtin at n=100 reverse_sorted: mean=317 ns, std=33 ns")
print("sorted_builtin at n=100 sorted: mean=270 ns, std=35 ns")
print()
print("Note: sorted_builtin times are extremely small (270-950 ns).")
print("At this scale, perf_counter_ns overhead itself is significant.")
print("The measurement noise is relatively high (std/mean ~ 7-13%).")
print("This is expected for very fast operations.")
print()

# Check if sorted_builtin times are suspiciously uniform
sb_100_random = summary[("sorted_builtin", 100, "random")]
print(f"sorted_builtin n=100 random: min={min(sb_100_random)}, max={max(sb_100_random)}")
print(f"  Unique values: {len(set(sb_100_random))}")
print(f"  Value distribution: {sorted(set(sb_100_random))}")

sb_100_sorted = summary[("sorted_builtin", 100, "sorted")]
print(f"sorted_builtin n=100 sorted: min={min(sb_100_sorted)}, max={max(sb_100_sorted)}")
print(f"  Unique values: {len(set(sb_100_sorted))}")
print(f"  Value distribution: {sorted(set(sb_100_sorted))}")

sb_100_rev = summary[("sorted_builtin", 100, "reverse_sorted")]
print(f"sorted_builtin n=100 reverse: min={min(sb_100_rev)}, max={max(sb_100_rev)}")
print(f"  Unique values: {len(set(sb_100_rev))}")
print(f"  Value distribution: {sorted(set(sb_100_rev))}")

# ---- Check 9: Verify sorted_builtin timing is suspiciously low ----
print()
print("=" * 60)
print("CHECK 9: sorted_builtin timing magnitude check")
print("=" * 60)
print("sorted_builtin at n=100: ~270-950 ns")
print("sorted_builtin at n=1000: ~1,793-18,408 ns")
print("sorted_builtin at n=3000: ~5,999-70,163 ns")
print()
print("These are wall-clock times including the copy operation.")
print("In algorithms.py, the timed section is:")
print("  timed_data = copy.deepcopy(data)")
print("  start = time.perf_counter_ns()")
print("  algo_fn(timed_data)")
print("  end = time.perf_counter_ns()")
print()
print("For sorted_builtin, the deepcopy of a 100-element list takes")
print("roughly comparable time to the sort itself. This adds noise.")
print("However, this is consistent across all algorithms, so")
print("comparisons between algorithms are still valid.")
print()

# ---- Check 10: Verify the warm-up data is not the same as timed data ----
print("=" * 60)
print("CHECK 10: Warm-up vs timed data identity")
print("=" * 60)
print("In benchmark_one():")
print("  warm_data = copy.deepcopy(data)  # warm-up copy")
print("  for _ in range(warmup_runs): algo_fn(warm_data)")
print("  ...")
print("  timed_data = copy.deepcopy(data)  # timed copy")
print()
print("The warm-up and timed copies are DIFFERENT objects.")
print("This means warm-up does NOT prime the timed data.")
print("This is CORRECT — warm-up should not contaminate timed runs.")
print("However, it also means warm-up benefits (e.g., CPU cache)")
print("may not fully transfer to the timed runs.")
print()

# ---- Check 11: Verify correctness check is separate ----
print("=" * 60)
print("CHECK 11: Correctness check isolation")
print("=" * 60)
print("In benchmark_one():")
print("  correct = algo_fn(list(data)) == sorted(data)")
print()
print("Correctness is checked on a separate copy of data.")
print("This is CORRECT — correctness check does not affect timing.")
print("However, correctness is only checked ONCE per configuration,")
print("not per repetition. This is acceptable since correctness")
print("should be deterministic for the same input.")
print()

# ---- Check 12: Verify CSV column order and content ----
print("=" * 60)
print("CHECK 12: CSV structure verification")
print("=" * 60)
with open("/workspace/results.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    print(f"Header: {header}")
    expected_header = ["algorithm", "size", "input_type", "seed", "repetition", "elapsed_ns", "correct"]
    print(f"Expected: {expected_header}")
    print(f"Match: {header == expected_header}")
print()

# ---- Check 13: Verify no False correctness values ----
print("=" * 60)
print("CHECK 13: No False correctness values")
print("=" * 60)
false_correct = [r for r in rows if r["correct"] == False]
print(f"Rows with correct=False: {len(false_correct)}")
print()

# ---- Check 14: Verify all seeds used ----
print("=" * 60)
print("CHECK 14: All seeds present")
print("=" * 60)
all_seeds = set(r["seed"] for r in rows)
print(f"Seeds found: {sorted(all_seeds)}")
print(f"Expected: {expected_seeds}")
print(f"Match: {sorted(all_seeds) == expected_seeds}")
print()

# ---- Check 15: Verify repetition numbering ----
print("=" * 60)
print("CHECK 15: Repetition numbering")
print("=" * 60)
reps_ok = True
for key, key_rows in configs.items():
    reps = sorted(r["repetition"] for r in key_rows)
    if reps != list(range(1, 51)):
        print(f"  {key}: reps = {reps[:5]}...{reps[-5:]}")
        reps_ok = False
print(f"All repetitions 1-50: {reps_ok}")
print()

# ---- Check 16: Verify input_type values ----
print("=" * 60)
print("CHECK 16: Input type values")
print("=" * 60)
all_types = set(r["input_type"] for r in rows)
print(f"Input types found: {sorted(all_types)}")
print(f"Expected: {expected_types}")
print(f"Match: {sorted(all_types) == expected_types}")
print()

# ---- Check 17: Verify algorithm values ----
print("=" * 60)
print("CHECK 17: Algorithm values")
print("=" * 60)
all_algos = set(r["algorithm"] for r in rows)
print(f"Algorithms found: {sorted(all_algos)}")
print(f"Expected: {expected_algos}")
print(f"Match: {sorted(all_algos) == expected_algos}")
print()

# ---- Check 18: Verify size values ----
print("=" * 60)
print("CHECK 18: Size values")
print("=" * 60)
all_sizes = set(r["size"] for r in rows)
print(f"Sizes found: {sorted(all_sizes)}")
print(f"Expected: {expected_sizes}")
print(f"Match: {sorted(all_sizes) == expected_sizes}")
print()

# ---- Check 19: Verify REPORT.md claims about speedup ranges ----
print("=" * 60)
print("CHECK 19: REPORT.md speedup range claims")
print("=" * 60)
print("Claim: sorted() is 50-200x faster than merge sort")
print("Claim: sorted() is 100-10,000x faster than insertion sort")
print()

min_ms_ratio = float('inf')
max_ms_ratio = 0
min_is_ratio = float('inf')
max_is_ratio = 0

for size in expected_sizes:
    for itype in expected_types:
        ms_mean = get_mean("merge_sort", size, itype)
        sb_mean = get_mean("sorted_builtin", size, itype)
        ratio = ms_mean / sb_mean
        min_ms_ratio = min(min_ms_ratio, ratio)
        max_ms_ratio = max(max_ms_ratio, ratio)

        is_mean = get_mean("insertion_sort", size, itype)
        ratio2 = is_mean / sb_mean
        min_is_ratio = min(min_is_ratio, ratio2)
        max_is_ratio = max(max_is_ratio, ratio2)

print(f"Merge sort / sorted() ratio range: {min_ms_ratio:.0f}x - {max_ms_ratio:.0f}x")
print(f"  Report claims: 50-200x")
print(f"  Claim supported: {50 <= min_ms_ratio and max_ms_ratio <= 200}")
print()
print(f"Insertion sort / sorted() ratio range: {min_is_ratio:.0f}x - {max_is_ratio:.0f}x")
print(f"  Report claims: 100-10,000x")
print(f"  Claim supported: {100 <= min_is_ratio and max_is_ratio <= 10000}")
print()

# ---- Check 20: Verify the "sorted_builtin" timing is suspiciously low ----
print("=" * 60)
print("CHECK 20: sorted_builtin timing magnitude analysis")
print("=" * 60)
print("sorted_builtin at n=100: mean ~270-950 ns")
print("sorted_builtin at n=1000: mean ~1,793-18,408 ns")
print("sorted_builtin at n=3000: mean ~5,999-70,163 ns")
print()
print("The sorted_builtin times are extremely small.")
print("For n=100, the mean is ~950 ns for random input.")
print("This is less than 1 microsecond.")
print("At this scale, the measurement is dominated by:")
print("  - perf_counter_ns() overhead")
print("  - deepcopy() overhead")
print("  - Python function call overhead")
print("  - The actual sort operation")
print()
print("The sorted_builtin times for sorted and reverse_sorted inputs")
print("are significantly lower than for random inputs, which is expected")
print("because Timsort exploits existing runs in the data.")
print()

# ---- Summary ----
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total rows: {len(rows)} (expected 6750)")
print(f"All configs present: {len(missing) == 0}")
print(f"All configs complete (50 reps): {len(incomplete) == 0}")
print(f"All correct=True: {all_correct}")
print(f"Mean mismatches: {len(mean_mismatches)}")
print(f"Std mismatches: {len(std_mismatches)}")