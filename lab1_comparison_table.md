| Algorithm | Theoretical bound | Measured trend (T/f ratio max n / min n) | Experimental limitations |
|---|---|---|---|
| list indexing | O(1) | 0.98 | Below timer resolution; needs inner-loop batching; cache effects at large n. |
| binary search | O(log n) | 1.20 | Tiny times, dominated by interpreter overhead; log growth looks almost flat. |
| linear search | O(n) | 1.02 | Worst case (absent key) only; average case differs by ~2x. |
| merge sort | O(n log n) | 1.06 | Slicing/allocation costs and GC add noise; recursion overhead in Python. |
| pair counter | O(n^2) | 1.30 | n limited to ~1600 because runtime grows 4x per doubling. |
| subset enumeration | O(2^n) | 0.89 | n limited to 16; has an extra factor n from the inner bit loop. |
