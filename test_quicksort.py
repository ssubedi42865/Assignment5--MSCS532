"""Correctness and partition checks. Run: python3 test_quicksort.py."""

import random
import unittest

from quicksort import partition, quicksort, randomized_quicksort


class QuicksortTests(unittest.TestCase):
    def test_sorts_and_in_place_contract(self):
        # Cover base cases, ordered inputs, duplicates, and negative numbers.
        cases = [[], [1], [2, 1], [3] * 100, [5, 4, 3, 2, 1],
                 list(range(100)), [0, -5, 3, -5, 2, 0]]
        rng = random.Random(42)
        cases += [[rng.randint(-100, 100) for _ in range(200)]
                  for _ in range(20)]
        # Fixed seeds make failures reproducible while exercising several
        # different random pivot sequences on the same test inputs.
        for sort_fn in (quicksort, randomized_quicksort):
            for seed in (0, 42, 99):
                random.seed(seed)
                for index, original in enumerate(cases):
                    with self.subTest(sort=sort_fn.__name__, seed=seed, case=index):
                        working = original[:]
                        result = sort_fn(working)
                        self.assertEqual(working, sorted(original))
                        self.assertIs(result, working)

    def test_partition_invariants(self):
        # Try every pivot index within an interior subarray. The sentinel
        # values at either end must remain untouched by partitioning.
        original = [999, 4, 2, 4, -1, 7, -999]
        for pivot_index in range(1, 6):
            with self.subTest(pivot_index=pivot_index):
                working = original[:]
                pivot_value = original[pivot_index]
                p = partition(working, 1, 5, pivot_index)
                self.assertEqual(working[p], pivot_value)
                self.assertTrue(all(x < pivot_value for x in working[1:p]))
                self.assertTrue(all(x >= pivot_value for x in working[p + 1:6]))
                # Sorting the ranges also checks that no values were lost.
                self.assertEqual(sorted(working[1:6]), sorted(original[1:6]))
                self.assertEqual(working[0], original[0])
                self.assertEqual(working[6], original[6])


if __name__ == "__main__":
    unittest.main(verbosity=2)
