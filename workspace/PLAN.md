# Experiment Plan: Sorting Algorithm Benchmark

## Research Question
How do input size and input order affect the running time of insertion sort, merge sort, and Python's built-in sorted()?

## Algorithms to Implement
1. **Insertion Sort** — O(n²) worst/average, O(n) best (already sorted)
2. **Merge Sort** — O(n log n) worst/average/best
3. **Python's built-in sorted()** — Timsort (hybrid of merge sort + insertion sort), implemented in C

## Methodology

### Correctness Verification
- Test cases: empty input, duplicates, negative numbers, already-sorted, reverse-sorted, single element
- Compare each algorithm's output against Python's `sorted()` on identical inputs
- Record pass/fail for each test

### Benchmark Design
- **Input sizes**: 100, 1000, 3000
- **Input types**: random, sorted (ascending), reverse-sorted (descending)
- **Random seeds**: 5 fixed seeds (e.g., 42, 123, 456, 789, 1000)
- **Repetitions**: 50 per configuration to reduce noise
- **Warm-up**: 10 runs before timing begins
- **Timing**: `time.perf_counter_ns()` for nanosecond precision
- **Input sharing**: Each algorithm receives an identical copy of the same input data

### Experimental Matrix
- 3 sizes × 3 input types × 5 seeds × 3 algorithms × 50 repetitions = 6,750 measurements

### Data Collection
- Save every individual measurement to `results.csv`
- Columns: algorithm, size, input_type, seed, repetition, elapsed_ns, correct

### Analysis Plan
- Compute mean and standard deviation per (algorithm, size, input_type)
- Compare how each algorithm scales with input size
- Compare how each algorithm handles different input orders
- Note: sorted() is C-implemented Timsort, so it will be faster than pure-Python implementations

## Limitations
- Pure Python implementations vs C-implemented sorted() is not a fair algorithm-design comparison
- Python interpreter overhead affects all pure-Python algorithms similarly
- No hardware-level profiling (cache, branch prediction)
- Single machine, single Python version

## Reproduction
```bash
cd /workspace
python3 algorithms.py
```
