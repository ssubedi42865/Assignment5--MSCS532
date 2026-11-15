"""Compare both sorts on distinct integers. Run: python3 benchmark.py."""

import platform
import random
import time

from quicksort import quicksort, randomized_quicksort

SIZES = [1000, 2000, 4000, 8000]
TRIALS = 3
SEED = 42


def make_input(kind, n, rng):
    """Create the requested ordering of the same n distinct integer keys."""
    data = list(range(n))
    if kind == "random":
        rng.shuffle(data)
    elif kind == "reverse-sorted":
        data.reverse()
    elif kind != "sorted":
        raise ValueError("Unknown input distribution: " + kind)
    return data


def time_sort(sort_fn, data):
    """Return the minimum sorting time across TRIALS, in seconds."""
    expected = sorted(data)
    best = float("inf")
    for _ in range(TRIALS):
        # Each run needs a fresh copy: the sorting functions modify their input.
        working = data[:]
        # Exclude input copying and correctness checking from the timed region.
        start = time.perf_counter()
        sort_fn(working)
        elapsed = time.perf_counter() - start
        if working != expected:
            raise AssertionError("Sort produced incorrect output")
        best = min(best, elapsed)
    # The minimum reduces interference from background work, but is not an
    # average or an estimate of expected runtime over all random pivot choices.
    return best


def main():
    # Separate input generation from pivot randomness so pivot draws cannot
    # change the random arrays generated for later benchmark cases.
    input_rng = random.Random(SEED)
    random.seed(SEED)
    print("Python:", platform.python_version())
    print("System:", platform.platform())
    print("Processor:", platform.processor() or platform.machine())
    print(f"Seed: {SEED}; minimum of {TRIALS} trials; times in seconds")
    print(f"{'distribution':<15}{'n':>7}{'deterministic (s)':>20}{'randomized (s)':>17}")
    for kind in ("random", "sorted", "reverse-sorted"):
        for n in SIZES:
            data = make_input(kind, n, input_rng)
            # Both algorithms receive copies of exactly the same input.
            det = time_sort(quicksort, data)
            rnd = time_sort(randomized_quicksort, data)
            print(f"{kind:<15}{n:>7}{det:>20.5f}{rnd:>17.5f}")


if __name__ == "__main__":
    main()
