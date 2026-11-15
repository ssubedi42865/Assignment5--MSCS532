# Assignment 5: Quicksort Implementation, Analysis, and Randomization

Python implementations of deterministic and randomized Quicksort, with a correctness test and an empirical benchmark.

## Files

- `quicksort.py` – `quicksort` (last-element pivot) and `randomized_quicksort` (uniformly random pivot). Both are in place and use a shared Lomuto partition. They recurse on the smaller side and loop on the larger, so stack depth is O(log n).
- `test_quicksort.py` – checks sorting correctness, in-place behavior, and partition invariants.
- `benchmark.py` – times both versions on random, sorted, and reverse-sorted inputs.
- `Quicksort_Report.docx` – the written report.

## How to run

Requires Python 3.8+ and no external packages.

```
python3 test_quicksort.py   # finishes with OK.
python3 benchmark.py        # prints the timing table
```

Benchmarks ran using Python 3.9.6 on macOS 26.6.2 with ARM architecture. Input sizes were 1,000, 2,000, 4,000, and 8,000 elements. Results are reported from the minimum of three trials with random seed 42. Input copying and correctness checks were excluded from timing.

## Summary of findings

| Case | Deterministic | Randomized |
|---|---|---|
| Random input | O(n log n) | O(n log n) expected |
| Sorted / reverse-sorted input | O(n²) | O(n log n) expected |

The O(n log n) average and expected bounds assume distinct keys. Both versions retain an O(n²) worst case. With this two-way partition, all-equal inputs take Θ(n²), even with randomized pivots.

Execution times for 8,000 elements (minimum of three trials).
| Input | Deterministic | Randomized |
|---|---:|---:|
| Random | 0.00745 s | 0.00883 s |
| Sorted | 1.98259 s | 0.00871 s |
| Reverse-sorted | 1.31683 s | 0.00853 s |
