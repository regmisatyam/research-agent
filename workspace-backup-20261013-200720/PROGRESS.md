# PROGRESS.md — Sorting Algorithm Benchmark

## Session Log

### Step 1: Planning ✅
- **Time**: Start of session
- **Action**: Read TASK.md, created PLAN.md
- **Details**: Defined experiment design — 3 algorithms (insertion_sort, merge_sort, sorted), 3 sizes (100, 1000, 3000), 3 input types (random, sorted, reverse_sorted), 5 seeds, 50 repetitions = 6,750 measurements
- **Evidence**: `/workspace/PLAN.md` created

### Step 2: Implementation ✅
- **Time**: After planning
- **Action**: Created `algorithms.py` with:
  - `insertion_sort()` — pure Python, in-place
  - `merge_sort()` — pure Python, top-down recursive
  - `sorted` — Python built-in (Timsort, C-implemented)
  - Correctness test suite (11 test cases)
  - Benchmark driver with warm-up, perf_counter_ns(), identical inputs
- **Evidence**: `/workspace/algorithms.py` created (220 lines)

### Step 3: Correctness Verification ✅
- **Time**: During first run
- **Action**: Ran `python3 algorithms.py`
- **Result**: All 33 correctness tests PASSED (3 algorithms × 11 test cases)
- **Test cases**: empty, single, two_elements, two_equal, duplicates, negatives, mixed_neg_pos, already_sorted, reverse_sorted, all_same, large_random
- **Evidence**: Console output in execution log

### Step 4: Benchmark Execution ✅
- **Time**: During first run
- **Action**: Full benchmark completed — all 6,750 measurements collected
- **Result**: All measurements saved to `results.csv` (6,751 lines including header)
- **Evidence**: `/workspace/results.csv` created
- **Summary output** (mean elapsed_ns):
  - insertion_sort: 2,913 ns (n=100 sorted) → 129,215,162 ns (n=3000 reverse)
  - merge_sort: 34,842 ns (n=100 sorted) → 2,064,942 ns (n=3000 random)
  - sorted_builtin: 270 ns (n=100 sorted) → 70,163 ns (n=3000 random)

### Step 5: Report Writing ✅
- **Time**: After benchmark completion
- **Action**: Created REPORT.md with:
  - Measured results table (all 27 configurations)
  - Key observations on input size and input order effects
  - Methodology description
  - Limitations (implementation language, interpreter overhead, etc.)
  - Reproduction instructions
- **Evidence**: `/workspace/REPORT.md` created

### Step 6: Progress Documentation ✅
- **Time**: Now
- **Action**: Created this PROGRESS.md
- **Status**: All deliverables complete

## Completed Deliverables
- [x] PLAN.md — Experiment plan written before running experiments
- [x] algorithms.py — All three algorithms implemented
- [x] Correctness verified against sorted() on 11 test cases (all passed)
- [x] Benchmark: 3 sizes × 3 input types × 5 seeds × 3 algorithms × 50 reps = 6,750 measurements
- [x] results.csv — All individual measurements saved
- [x] REPORT.md — Results, methodology, limitations, reproduction instructions
- [x] sorted() vs pure-Python limitation explicitly explained
- [x] PROGRESS.md — This file

## Failures / Issues
- None. All experiments completed successfully on first run.

## Next Actions
- None. All deliverables are complete.
