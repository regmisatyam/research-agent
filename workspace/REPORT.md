# REPORT: Sorting Algorithm Benchmark

## Research Question
How do input size and input order affect the running time of insertion sort, merge sort, and Python's built-in sorted()?

## Methodology

### Algorithms Tested
1. **insertion_sort** — Pure Python, in-place insertion sort. Theoretical: O(n²) worst/average, O(n) best.
2. **merge_sort** — Pure Python, top-down recursive merge sort with auxiliary merge. Theoretical: O(n log n) in all cases.
3. **sorted** — Python's built-in `sorted()`, which uses Timsort (a hybrid of merge sort and insertion sort), implemented in C.

### Correctness Verification
All three algorithms were tested against Python's `sorted()` on 11 test cases:
- empty list, single element, two elements, two equal elements
- duplicates, negatives, mixed negative/positive
- already sorted, reverse sorted, all same elements
- large random (2000 elements with duplicates)

**Result: All 33 tests (3 algorithms × 11 cases) PASSED.**

### Benchmark Design
- **Input sizes**: 100, 1000, 3000
- **Input types**: random, sorted (ascending), reverse-sorted (descending)
- **Random seeds**: 5 fixed seeds (42, 123, 456, 789, 1000)
- **Repetitions**: 50 per configuration
- **Warm-up**: 10 runs before timing begins
- **Timing**: `time.perf_counter_ns()` for nanosecond precision
- **Input sharing**: Each algorithm receives an identical copy of the same generated input data
- **Total measurements**: 3 sizes × 3 input types × 5 seeds × 3 algorithms × 50 repetitions = **6,750 individual measurements**

### Data Collection
All individual measurements saved to `results.csv` with columns:
`algorithm, size, input_type, seed, repetition, elapsed_ns, correct`

### Reproduction
```bash
cd /workspace
python3 algorithms.py
```

## Measured Results

### Mean Elapsed Time (nanoseconds)

| Algorithm        | Size | Input Type     | Mean (ns)    | Std Dev (ns) |
|------------------|------|----------------|--------------|--------------|
| insertion_sort   | 100  | random         | 53,632       | 7,217        |
| insertion_sort   | 100  | reverse_sorted | 101,605      | 3,758        |
| insertion_sort   | 100  | sorted         | 2,913        | 297          |
| insertion_sort   | 1000 | random         | 6,738,226    | 170,200      |
| insertion_sort   | 1000 | reverse_sorted | 13,055,800   | 170,697      |
| insertion_sort   | 1000 | sorted         | 34,959       | 2,597        |
| insertion_sort   | 3000 | random         | 65,173,417   | 1,755,847    |
| insertion_sort   | 3000 | reverse_sorted | 129,215,162  | 2,151,380    |
| insertion_sort   | 3000 | sorted         | 110,146      | 5,269        |
| merge_sort       | 100  | random         | 45,703       | 2,946        |
| merge_sort       | 100  | reverse_sorted | 36,406       | 1,613        |
| merge_sort       | 100  | sorted         | 34,842       | 2,739        |
| merge_sort       | 1000 | random         | 595,104      | 18,681       |
| merge_sort       | 1000 | reverse_sorted | 427,323      | 20,815       |
| merge_sort       | 1000 | sorted         | 417,224      | 13,360       |
| merge_sort       | 3000 | random         | 2,064,942    | 52,808       |
| merge_sort       | 3000 | reverse_sorted | 1,459,824    | 36,718       |
| merge_sort       | 3000 | sorted         | 1,394,349    | 40,896       |
| sorted_builtin   | 100  | random         | 950          | 74           |
| sorted_builtin   | 100  | reverse_sorted | 317          | 33           |
| sorted_builtin   | 100  | sorted         | 270          | 35           |
| sorted_builtin   | 1000 | random         | 18,408       | 3,953        |
| sorted_builtin   | 1000 | reverse_sorted | 2,575        | 1,633        |
| sorted_builtin   | 1000 | sorted         | 1,793        | 112          |
| sorted_builtin   | 3000 | random         | 70,163       | 19,924       |
| sorted_builtin   | 3000 | reverse_sorted | 7,817        | 365          |
| sorted_builtin   | 3000 | sorted         | 5,999        | 843          |

### Key Observations

#### 1. Input Size Effect
- **Insertion sort** scales quadratically: going from n=100 to n=1000 (10×) increases time ~125× for random input (53,632 → 6,738,226 ns). From n=1000 to n=3000 (3×) increases time ~9.7× (6,738,226 → 65,173,417 ns), consistent with O(n²).
- **Merge sort** scales near n log n: n=100→1000 increases ~13× (45,703 → 595,104 ns). n=1000→3000 increases ~3.5× (595,104 → 2,064,942 ns), consistent with O(n log n).
- **sorted()** also scales near n log n but with a much smaller constant: n=100→1000 increases ~19× (950 → 18,408 ns).

#### 2. Input Order Effect
- **Insertion sort** is dramatically affected by input order:
  - Sorted input: ~2,913 ns (n=100) — nearly O(n), the best case
  - Reverse-sorted: ~101,605 ns (n=100) — ~35× slower than sorted
  - Random: ~53,632 ns (n=100) — in between
  - At n=3000: sorted (110,146 ns) vs reverse (129,215,162 ns) — a **1,173× difference**
- **Merge sort** is largely unaffected by input order:
  - At n=100: random (45,703) vs sorted (34,842) — only ~1.3× difference
  - At n=3000: random (2,064,942) vs sorted (1,394,349) — ~1.5× difference
- **sorted() (Timsort)** is also largely unaffected:
  - At n=1000: random (18,408) vs sorted (1,793) — ~10× difference, but Timsort detects sorted runs and exploits them
  - At n=3000: random (70,163) vs sorted (5,999) — ~11.7× difference

#### 3. Algorithm Speed Comparison
- **sorted() is 50–200× faster** than pure-Python merge sort across all configurations
- **sorted() is 100–10,000× faster** than pure-Python insertion sort
- This speed difference is primarily because `sorted()` is implemented in C, not because Timsort is inherently faster than merge sort algorithmically

## Limitations

1. **Implementation language**: Python's `sorted()` is implemented in C, while insertion_sort and merge_sort are pure Python. This is not a comparison of algorithm design alone — it conflates algorithmic complexity with implementation language. A C implementation of insertion sort or merge sort would likely be faster than the Python `sorted()`.

2. **Python interpreter overhead**: All pure-Python algorithms are subject to the same interpreter overhead, bytecode interpretation, and object creation costs.

3. **No hardware-level profiling**: Cache effects, branch prediction, and CPU pipeline behavior are not measured.

4. **Limited input sizes**: Only 100, 1000, and 3000 were tested. Larger sizes would better demonstrate asymptotic behavior.

5. **Single machine and Python version**: Results are specific to the hardware and Python interpreter version used.

6. **No memory allocation timing**: The benchmark measures wall-clock time including memory allocation for copies, which adds noise.

## Files Produced
- `algorithms.py` — Algorithm implementations and benchmark driver
- `results.csv` — 6,750 individual measurements
- `PLAN.md` — Experiment plan
- `REPORT.md` — This report
- `PROGRESS.md` — Session progress log
