"""
Assignment 2 - Algorithm Analysis: Laboratory Works (complete)
Name: Aditya Raj | Roll No: 25BEC007

Contains BOTH laboratory works in one file:
  Lab Work 1 : Benchmarking Algorithmic Growth Rates
  Lab Work 2 : Prefix Averages - Quadratic versus Linear-Time Design

Run:  python Assignment_2_Lab_Works.py            (both labs, full run)
      python Assignment_2_Lab_Works.py --quick    (both labs, small sizes)
      python Assignment_2_Lab_Works.py 1|2        (only one lab; combine with --quick)
Plots / CSV / table are written next to this file.
"""
import sys, os, platform, time, random, math, statistics, csv



##############################################################################
# LAB WORK 1 - Benchmarking Algorithmic Growth Rates
##############################################################################
# Lab Work 1: Benchmarking Algorithmic Growth Rates
# Name: Aditya Raj | Roll No: 25BEC007
# 
# Run:  python Lab1_Benchmarking_Growth_Rates.py          (full run)
#       python Lab1_Benchmarking_Growth_Rates.py --quick  (small sizes, fast check)
# 
# Methodology
# - Input generation/validation is done OUTSIDE the timed region.
# - Each (algorithm, n) is timed `REPEATS` times; the reported value is the MEDIAN.
# - Fast operations (indexing) are repeated `inner` times per trial and divided,
#   because a single call is below timer resolution.
# - Random inputs use a fixed seed (reproducible).


SEED = 25007
REPEATS = 7


# ---------------------------- algorithms ----------------------------------
def list_index(data, idx):                       # O(1)
    return data[idx]


def binary_search(a, target):                    # O(log n), a sorted
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def linear_search(a, target):                    # O(n)
    for i, v in enumerate(a):
        if v == target:
            return i
    return -1


def merge_sort(a):                               # O(n log n)
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:]); out.extend(right[j:])
    return out


def pair_counter(a, target):                     # O(n^2)
    count = 0
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] + a[j] == target:
                count += 1
    return count


def subset_enumeration(items):                   # O(2^n) -- small n only
    n = len(items)
    total = 0
    for mask in range(1 << n):
        s = 0
        for b in range(n):
            if mask >> b & 1:
                s += items[b]
        total += s
    return total


# ---------------------------- timing harness ------------------------------
def measure(run, repeats=REPEATS, inner=1):
    """run: zero-arg callable (inputs already prepared). Returns median sec/call."""
    trials = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        for _ in range(inner):
            run()
        trials.append((time.perf_counter() - t0) / inner)
    return statistics.median(trials)


def build_experiments(quick):
    rng = random.Random(SEED)
    sc = 0.1 if quick else 1.0
    def sizes(lst): return [max(2, int(x * sc)) for x in lst]
    exps = []

    def mk_index(n):
        d = list(range(n)); i = n // 2
        return lambda: list_index(d, i)
    def mk_bin(n):
        d = list(range(n)); t = -1                     # worst case: absent
        return lambda: binary_search(d, t)
    def mk_lin(n):
        d = list(range(n)); t = -1                     # worst case: absent
        return lambda: linear_search(d, t)
    def mk_msort(n):
        d = [rng.randint(0, 10**6) for _ in range(n)]
        return lambda: merge_sort(d)
    def mk_pair(n):
        d = [rng.randint(0, 10**6) for _ in range(n)]
        return lambda: pair_counter(d, -1)             # no pair sums to -1
    def mk_subset(n):
        d = list(range(n))
        return lambda: subset_enumeration(d)

    exps.append(("list indexing", "O(1)", mk_index, [10**3, 10**4, 10**5, 10**6, 10**7] if not quick else [10**3, 10**4, 10**5], 2000))
    exps.append(("binary search", "O(log n)", mk_bin, [10**3, 10**4, 10**5, 10**6, 10**7] if not quick else [10**3, 10**4, 10**5], 500))
    exps.append(("linear search", "O(n)", mk_lin, sizes([10**4, 5*10**4, 10**5, 5*10**5, 10**6]), 1))
    exps.append(("merge sort", "O(n log n)", mk_msort, sizes([10**3, 5*10**3, 10**4, 5*10**4, 10**5]), 1))
    exps.append(("pair counter", "O(n^2)", mk_pair, sizes([100, 200, 400, 800, 1600]), 1))
    exps.append(("subset enumeration", "O(2^n)", mk_subset, [8, 10, 12, 14, 16] if not quick else [6, 8, 10], 1))
    return exps


def normaliser(name):
    return {
        "list indexing": lambda n: 1,
        "binary search": lambda n: math.log2(n),
        "linear search": lambda n: n,
        "merge sort": lambda n: n * math.log2(n),
        "pair counter": lambda n: n * n,
        "subset enumeration": lambda n: n * 2 ** n,   # inner bit loop adds factor n
    }[name]


def lab1_main():
    quick = "--quick" in sys.argv
    here = os.path.dirname(os.path.abspath(__file__))
    print(f"Python {platform.python_version()} on {platform.platform()}")
    print(f"Repeats per point: {REPEATS}; statistic: MEDIAN; seed: {SEED}\n")

    results = {}
    rows = []
    for name, bound, maker, ns, inner in build_experiments(quick):
        pts = []
        for n in ns:
            run = maker(n)                      # data generation (untimed)
            t = measure(run, inner=inner)
            pts.append((n, t))
            rows.append((name, bound, n, t))
            print(f"{name:20s} n={n:>9d}  t={t:.3e} s")
        results[name] = (bound, pts)
        print()

    with open(os.path.join(here, "lab1_timing_data.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["algorithm", "bound", "n", "median_seconds"]); w.writerows(rows)

    # Trend check: ratio of normalised time at largest vs smallest n (~1 => matches bound)
    print("Normalised-time stability  [T(n)/f(n) at max n  divided by  at min n]")
    summary = {}
    for name, (bound, pts) in results.items():
        f = normaliser(name)
        r = (pts[-1][1] / f(pts[-1][0])) / (pts[0][1] / f(pts[0][0]))
        summary[name] = r
        print(f"  {name:20s} {bound:11s} ratio = {r:.2f}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(2, 3, figsize=(14, 8))
        for ax, (name, (bound, pts)) in zip(axes.flat, results.items()):
            ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-")
            ax.set_title(f"{name} — {bound}"); ax.set_xlabel("n"); ax.set_ylabel("time (s)")
            ax.grid(alpha=.3)
        fig.tight_layout(); fig.savefig(os.path.join(here, "lab1_time_vs_n.png"), dpi=130)

        fig, axes = plt.subplots(2, 3, figsize=(14, 8))
        for ax, (name, (bound, pts)) in zip(axes.flat, results.items()):
            f = normaliser(name)
            ax.plot([p[0] for p in pts], [p[1] / f(p[0]) for p in pts], "s-", color="tab:red")
            ax.set_title(f"{name}: T(n)/f(n), f = {bound}"); ax.set_xlabel("n")
            ax.set_ylim(bottom=0); ax.grid(alpha=.3)
        fig.tight_layout(); fig.savefig(os.path.join(here, "lab1_normalised.png"), dpi=130)
        print("\nSaved plots: lab1_time_vs_n.png, lab1_normalised.png")
    except ImportError:
        print("matplotlib not installed - skipping plots (pip install matplotlib)")

    limits = {
        "list indexing": "Below timer resolution; needs inner-loop batching; cache effects at large n.",
        "binary search": "Tiny times, dominated by interpreter overhead; log growth looks almost flat.",
        "linear search": "Worst case (absent key) only; average case differs by ~2x.",
        "merge sort": "Slicing/allocation costs and GC add noise; recursion overhead in Python.",
        "pair counter": "n limited to ~1600 because runtime grows 4x per doubling.",
        "subset enumeration": "n limited to 16; has an extra factor n from the inner bit loop.",
    }
    with open(os.path.join(here, "lab1_comparison_table.md"), "w") as f:
        f.write("| Algorithm | Theoretical bound | Measured trend (T/f ratio max n / min n) | Experimental limitations |\n|---|---|---|---|\n")
        for name, (bound, _) in results.items():
            f.write(f"| {name} | {bound} | {summary[name]:.2f} | {limits[name]} |\n")
    print("Saved lab1_comparison_table.md and lab1_timing_data.csv")


##############################################################################
# LAB WORK 2 - Prefix Averages: Quadratic vs Linear
##############################################################################
# Lab Work: Prefix Averages — Quadratic versus Linear-Time Design
# Name: Aditya Raj | Roll No: 25BEC007
# 
# Run:  python Lab2_Prefix_Averages.py          (tests + benchmark + plot)
#       python Lab2_Prefix_Averages.py --quick
# 
# Empty-input handling: both functions return [] for an empty sequence.
# 
# Derivations (operation counts)
# ------------------------------
# prefix_average1: for each j in 0..n-1 the inner loop performs (j+1) additions.
#     T1(n) = sum_{j=0}^{n-1} (j+1) = n(n+1)/2           -> Theta(n^2)
#     (plus n divisions and n appends: T1(n) = n(n+1)/2 + 2n)
# prefix_average2: one addition, one division, one append per element.
#     T2(n) = 3n                                          -> Theta(n)
# 
# Numerical precision
# -------------------
# Both use floating-point division. prefix_average1 re-sums each prefix from
# scratch (error grows ~ O(j*eps)), prefix_average2 accumulates one running
# total (error also ~ O(n*eps) but with a single rounding path). For integer
# inputs both totals are exact (Python ints), so results are identical; for
# floats tiny differences (~1e-16 relative) can arise, hence math.isclose is
# used in validation.



def prefix_average1(S):
    """Quadratic: recompute each prefix sum."""
    n = len(S)
    A = [0] * n
    for j in range(n):
        total = 0
        for i in range(j + 1):
            total += S[i]
        A[j] = total / (j + 1)
    return A


def prefix_average2(S):
    """Linear: maintain a running sum."""
    n = len(S)
    A = [0] * n
    total = 0
    for j in range(n):
        total += S[j]
        A[j] = total / (j + 1)
    return A


def validate():
    cases = {
        "empty": [],
        "singleton": [5],
        "positive": [1, 2, 3, 4, 5],
        "negative": [-1, -2, -3, -4],
        "mixed": [3, -3, 10, -20, 7, 0],
        "floats": [0.1, 0.2, 0.3, 0.4],
    }
    for name, S in cases.items():
        a, b = prefix_average1(S), prefix_average2(S)
        assert len(a) == len(b) == len(S), name
        assert all(math.isclose(x, y, rel_tol=1e-12, abs_tol=1e-12) for x, y in zip(a, b)), name
        print(f"  [PASS] {name:10s} {S} -> {b}")
    assert prefix_average1([1, 2, 3, 4, 5]) == [1, 1.5, 2, 2.5, 3]
    rng = random.Random(1)
    for _ in range(200):
        S = [rng.randint(-100, 100) for _ in range(rng.randint(0, 60))]
        assert prefix_average1(S) == prefix_average2(S)
    print("  [PASS] 200 random integer sequences identical")


def median_time(fn, S, repeats):
    ts = []
    for _ in range(repeats):
        t0 = time.perf_counter(); fn(S); ts.append(time.perf_counter() - t0)
    return statistics.median(ts)


def lab2_main():
    quick = "--quick" in sys.argv
    here = os.path.dirname(os.path.abspath(__file__))
    print(f"Python {platform.python_version()} on {platform.platform()}")
    print("Validation tests:"); validate()

    sizes = [100, 200, 400, 800, 1600, 3200] if not quick else [50, 100, 200, 400]
    big_sizes = [10**4, 10**5, 10**6] if not quick else [10**4, 10**5]   # linear only
    repeats = 7
    rng = random.Random(25007)
    rows = []
    print(f"\nMedian of {repeats} trials (seconds)")
    print(f"{'n':>8} {'prefix_average1':>16} {'prefix_average2':>16} {'speed-up':>9}")
    for n in sizes:
        S = [rng.randint(-1000, 1000) for _ in range(n)]      # untimed generation
        t1 = median_time(prefix_average1, S, repeats)
        t2 = median_time(prefix_average2, S, repeats)
        rows.append((n, t1, t2))
        print(f"{n:>8} {t1:>16.6f} {t2:>16.6f} {t1/t2:>8.1f}x")
    for n in big_sizes:
        S = [rng.randint(-1000, 1000) for _ in range(n)]
        t2 = median_time(prefix_average2, S, 3)
        print(f"{n:>8} {'(skipped O(n^2))':>16} {t2:>16.6f}")

    with open(os.path.join(here, "lab2_timing_data.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["n", "prefix_average1_s", "prefix_average2_s"]); w.writerows(rows)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        ns = [r[0] for r in rows]
        fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
        ax[0].plot(ns, [r[1] for r in rows], "o-", label="prefix_average1  O(n²)")
        ax[0].plot(ns, [r[2] for r in rows], "s-", label="prefix_average2  O(n)")
        ax[0].set_xlabel("n"); ax[0].set_ylabel("time (s)"); ax[0].legend(); ax[0].grid(alpha=.3)
        ax[0].set_title("Execution time vs n")
        ax[1].loglog(ns, [r[1] for r in rows], "o-", label="prefix_average1")
        ax[1].loglog(ns, [r[2] for r in rows], "s-", label="prefix_average2")
        c1, c2 = rows[0][1] / ns[0] ** 2, rows[0][2] / ns[0]
        ax[1].loglog(ns, [c1 * n * n for n in ns], "k--", alpha=.5, label="c·n² (slope 2)")
        ax[1].loglog(ns, [c2 * n for n in ns], "k:", alpha=.5, label="c·n (slope 1)")
        ax[1].set_xlabel("n"); ax[1].legend(); ax[1].grid(alpha=.3, which="both")
        ax[1].set_title("Log-log: slope reveals exponent")
        fig.tight_layout(); fig.savefig(os.path.join(here, "lab2_prefix_average_plot.png"), dpi=130)
        print("\nSaved lab2_prefix_average_plot.png")
    except ImportError:
        print("matplotlib not installed - skipping plot")

    # Empirical exponent via log-log slope
    if len(rows) >= 2:
        s1 = math.log(rows[-1][1] / rows[0][1]) / math.log(rows[-1][0] / rows[0][0])
        s2 = math.log(rows[-1][2] / rows[0][2]) / math.log(rows[-1][0] / rows[0][0])
        print(f"Empirical exponents: prefix_average1 ~ n^{s1:.2f}, prefix_average2 ~ n^{s2:.2f}")


if __name__ == "__main__":
    which = [a for a in sys.argv[1:] if a in ("1", "2")]
    if not which or "1" in which:
        print("=" * 70 + "\nLAB WORK 1: Benchmarking Algorithmic Growth Rates\n" + "=" * 70)
        lab1_main()
    if not which or "2" in which:
        print("\n" + "=" * 70 + "\nLAB WORK 2: Prefix Averages\n" + "=" * 70)
        lab2_main()
