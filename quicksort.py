"""In-place deterministic and randomized Quicksort using Lomuto partitioning.

Both versions modify the supplied list and return that same list. Elements
must support comparison with <. Swaps make these sorts unstable: equal-key
records are not guaranteed to keep their original relative order.
"""

import random


def partition(arr, low, high, pivot_index):
    """Partition the inclusive range low..high and return the pivot's position.

    Valid indices must satisfy 0 <= low <= pivot_index <= high < len(arr).
    One scan takes Theta(high - low + 1) time and O(1) extra space.
    """
    # Put the selected pivot at the end so the scan does not move it early.
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    pivot = arr[high]
    boundary = low

    # Before each iteration, low..boundary-1 contains values < pivot,
    # boundary..i-1 contains values >= pivot, and i..high-1 is unexamined.
    for i in range(low, high):
        if arr[i] < pivot:
            arr[i], arr[boundary] = arr[boundary], arr[i]
            boundary += 1

    # The pivot belongs between the smaller values and the remaining values.
    arr[boundary], arr[high] = arr[high], arr[boundary]
    return boundary


def _quicksort(arr, low, high, choose_pivot):
    """Sort one inclusive range using the supplied pivot-selection function."""
    # Empty and one-element ranges are already sorted (low >= high).
    while low < high:
        p = partition(arr, low, high, choose_pivot(low, high))

        # Position p is settled, so exclude it from both remaining ranges.
        # Only recurse on the smaller side: each nested call handles at most
        # half as many elements. Loop over the larger side to keep the stack
        # O(log n), even when the total sorting time becomes O(n^2).
        if p - low < high - p:
            _quicksort(arr, low, p - 1, choose_pivot)
            low = p + 1
        else:
            _quicksort(arr, p + 1, high, choose_pivot)
            high = p - 1


def quicksort(arr):
    """Sort in place with the last element as pivot; return the same list.

    Best time: Theta(n log n). Average over random permutations of distinct
    keys: Theta(n log n). Worst time: Theta(n^2), including sorted,
    reverse-sorted, and all-equal inputs. Auxiliary stack space: O(log n).
    """
    # A lambda supplies the pivot policy to the shared sorting driver.
    _quicksort(arr, 0, len(arr) - 1, lambda low, high: high)
    return arr


def randomized_quicksort(arr):
    """Sort in place with random pivots; return the same list.

    For distinct keys, expected time is Theta(n log n) for any fixed input
    order; the expectation is over the random pivot choices. Worst time
    remains Theta(n^2). With this two-way partition, all-equal inputs always
    take Theta(n^2), because equal values all stay on one side of the pivot.
    Auxiliary stack space is O(log n), as in the deterministic version.
    """
    # randint includes both endpoints, allowing every current index to be
    # selected with equal probability, rather than choosing from the full list.
    _quicksort(arr, 0, len(arr) - 1, lambda low, high: random.randint(low, high))
    return arr
