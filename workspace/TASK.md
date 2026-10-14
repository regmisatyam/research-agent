Research question:
How do input size and input order affect the running time of
insertion sort, merge sort, and Python's built-in sorted()?

Use Python's standard library only.

Requirements:
1. Write PLAN.md before running experiments.
2. Implement the algorithms in algorithms.py.
3. Verify correctness against sorted(), including empty inputs,
   duplicates, negative numbers, and already-sorted inputs.
4. Benchmark sizes 100, 1000, and 3000 with random, sorted, and
   reverse-sorted inputs. Use five fixed random seeds.
5. Give every algorithm identical input values for each comparison.
   Copy inputs outside the timed section. Use perf_counter_ns().
   Include warm-up runs and repeat measurements.
6. Save individual measurements to results.csv, including algorithm,
   size, input type, seed, repetition, elapsed time, and correctness.
7. Write REPORT.md with measured results, methodology, limitations,
   and instructions to reproduce the experiment.
8. Explain that built-in sorted() versus pure Python implementations
   is not a comparison of algorithm design alone.
9. Update PROGRESS.md after each major step. Record completed work,
   failures, evidence, and the next action.
10. Only report measurements actually produced by executed code.
    Do not claim novelty. Stop when the deliverables are complete.

Keep all work in /workspace.
