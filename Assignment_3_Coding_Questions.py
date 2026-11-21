"""
Assignment 3 - Data Structures and Algorithms with Python: Coding Questions (complete)
Name: Aditya Raj | Roll No: 25BEC007

All programming questions in one file:
  Part A - Recursion
  Part B - Array-Based Sequences
  Part C - Stacks, Queues and Deques
  Part D - Linked Lists

Run:  python Assignment_3_Coding_Questions.py          (all parts)
      python Assignment_3_Coding_Questions.py A        (only Part A; also B, C, D, or e.g. "A C")
"""
import sys
import copy
import ctypes
import time
from collections import deque

sys.setrecursionlimit(10000)



##############################################################################
# PART A - Recursion
##############################################################################
# Part A - Recursion (coding questions)
# Name: Aditya Raj | Roll No: 25BEC007
# Run: python recursion_assignments.py

sys.setrecursionlimit(10000)


# 1. factorial -- precondition: n is an int >= 0; base case: n == 0 -> 1
def factorial(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return 1
    return n * factorial(n - 1)


# 2. sum of first n natural numbers -- precondition n >= 0; base: n == 0 -> 0
def linear_sum(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return 0
    return n + linear_sum(n - 1)


# 3. x ** n for non-negative integer n -- base: n == 0 -> 1
def power(x, n):
    """Repeated squaring: O(log n) calls."""
    if n < 0 or int(n) != n:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 1
    half = power(x, n // 2)
    return half * half if n % 2 == 0 else x * half * half


# 4. reverse a sequence in place using start/stop (stop exclusive)
def reverse_inplace(S, start=0, stop=None, trace=False, depth=0):
    if stop is None:
        stop = len(S)
    if trace:
        print("  " * depth + f"reverse(start={start}, stop={stop}) S={S}")
    if start < stop - 1:                       # base: 0 or 1 element left
        S[start], S[stop - 1] = S[stop - 1], S[start]
        reverse_inplace(S, start + 1, stop - 1, trace, depth + 1)
    elif trace:
        print("  " * depth + f"base case reached, S={S}")


# 5. is sorted (non-decreasing)
def is_sorted(S, i=0):
    """Best case O(1) (first pair out of order); worst case O(n) (already sorted)."""
    if i >= len(S) - 1:
        return True
    if S[i] > S[i + 1]:
        return False
    return is_sorted(S, i + 1)


# 6. naive Fibonacci
def fib(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


calls = 0
def fib_counted(n):
    global calls
    calls += 1
    if n <= 1:
        return n
    return fib_counted(n - 1) + fib_counted(n - 2)


def fib_tree(n, prefix="", is_last=True, seen=None):
    """Print recursion tree; '*' marks a repeated subproblem."""
    if seen is None:
        seen = {}
    mark = "*" if n in seen else ""
    seen[n] = seen.get(n, 0) + 1
    print(prefix + ("└── " if is_last else "├── ") + f"fib({n}){mark}")
    if n > 1:
        ext = prefix + ("    " if is_last else "│   ")
        fib_tree(n - 1, ext, False, seen)
        fib_tree(n - 2, ext, True, seen)


# 7. Tower of Hanoi: 1) move n-1 disks src->aux  2) move disk n src->dst  3) move n-1 aux->dst
def hanoi(n, src="A", dst="C", aux="B", moves=None):
    if moves is None:
        moves = []
    if n == 0:                                 # base case
        return moves
    hanoi(n - 1, src, aux, dst, moves)
    moves.append((n, src, dst))
    hanoi(n - 1, aux, dst, src, moves)
    return moves


# 8/9. tail recursion and conversion to iteration
def binary_search_rec(S, target, low=0, high=None):      # TAIL recursive
    if high is None:
        high = len(S) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if S[mid] == target:
        return mid
    if S[mid] < target:
        return binary_search_rec(S, target, mid + 1, high)
    return binary_search_rec(S, target, low, mid - 1)


def binary_search_iter(S, target):                       # O(1) stack space
    low, high = 0, len(S) - 1
    while low <= high:
        mid = (low + high) // 2
        if S[mid] == target:
            return mid
        if S[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def reverse_iter(S):                                     # iterative version of reverse_inplace
    start, stop = 0, len(S)
    while start < stop - 1:
        S[start], S[stop - 1] = S[stop - 1], S[start]
        start, stop = start + 1, stop - 1


def factorial_tail(n, acc=1):                            # tail-recursive factorial (accumulator)
    return acc if n == 0 else factorial_tail(n - 1, acc * n)


def factorial_iter(n):
    acc = 1
    while n > 0:
        acc, n = acc * n, n - 1
    return acc


def stack_depth_demo():
    """Compare call-stack use: recursion O(n) frames vs loop O(1)."""
    depth = [0]
    def probe(n):
        depth[0] = max(depth[0], n)
        if n < 500:
            probe(n + 1)
    probe(0)
    return depth[0] + 1


def part_a_main():
    print("== 2. factorial / linear_sum / power ==")
    print("factorial(0..6):", [factorial(i) for i in range(7)])
    print("linear_sum(10) =", linear_sum(10), "(expected 55)")
    print("power(2, 10) =", power(2, 10), "| power(3, 0) =", power(3, 0), "| power(5, 3) =", power(5, 3))

    print("\n== 3. reverse in place, 6 elements, trace ==")
    S = [1, 2, 3, 4, 5, 6]
    reverse_inplace(S, trace=True)
    print("Result:", S)

    print("\n== 4. is_sorted ==")
    for t in ([], [1], [1, 2, 2, 5], [3, 1, 2], [1, 2, 3, 2]):
        print(f"is_sorted({t}) = {is_sorted(t)}")

    print("\n== 5. Fibonacci recursion tree n=5 (* = repeated subproblem) ==")
    fib_tree(5)
    print("fib(0..10):", [fib(i) for i in range(11)])

    print("\n== 6. number of calls made by naive fib ==")
    global calls
    print(f"{'n':>3} {'fib(n)':>8} {'calls':>8}")
    for n in range(1, 21, 2):
        calls = 0
        v = fib_counted(n)
        print(f"{n:>3} {v:>8} {calls:>8}   (= 2*fib(n+1)-1 = {2*fib(n+1)-1})")

    print("\n== 7. Tower of Hanoi ==")
    for n in (1, 2, 3):
        mv = hanoi(n)
        print(f"n={n}: {len(mv)} moves (2^n-1 = {2**n-1})")
    print("n=3 moves:", [f"disk{d}:{s}->{t}" for d, s, t in hanoi(3)])

    print("\n== 9. tail recursion -> iteration ==")
    data = list(range(0, 100, 3))
    print("binary_search_rec:", binary_search_rec(data, 27), "| iter:", binary_search_iter(data, 27))
    print("binary_search_rec missing:", binary_search_rec(data, 28), "| iter:", binary_search_iter(data, 28))
    T = [1, 2, 3, 4, 5]; reverse_iter(T); print("reverse_iter:", T)
    print("factorial_tail(10) =", factorial_tail(10), "| factorial_iter(10) =", factorial_iter(10))
    print(f"Call-stack frames used by recursive version for depth 500: {stack_depth_demo()}  vs iterative: 1")


##############################################################################
# PART B - Array-Based Sequences
##############################################################################
# Part B - Array-Based Sequences (coding questions)
# Name: Aditya Raj | Roll No: 25BEC007
# Run: python array_sequences_assignments.py



# ---- Shallow vs deep copy on a nested list -------------------------------
def copy_demo():
    original = [[1, 2], [3, 4], 5]
    shallow = copy.copy(original)            # also: original[:] or list(original)
    deep = copy.deepcopy(original)

    original[0].append(99)                   # mutate an INNER mutable object
    original[2] = 500                        # rebind an outer slot (immutable int)

    print("original :", original)
    print("shallow  :", shallow, "<- inner list shared, so it sees 99; slot 2 unaffected")
    print("deep     :", deep, "<- fully independent")
    print("shallow[0] is original[0] ->", shallow[0] is original[0])
    print("deep[0]    is original[0] ->", deep[0] is original[0])


# ---- Dynamic array: resize when full -------------------------------------
class DynamicArray:
    """Array-backed list with capacity doubling (amortised O(1) append)."""

    def __init__(self):
        self._n = 0
        self._capacity = 1
        self._A = self._make_array(self._capacity)

    @staticmethod
    def _make_array(c):
        return (c * ctypes.py_object)()

    def __len__(self):
        return self._n

    def __getitem__(self, k):
        if not -self._n <= k < self._n:
            raise IndexError("invalid index")
        return self._A[k % self._n if k < 0 else k]

    def append(self, obj):
        if self._n == self._capacity:                  # 1. array is full
            self._resize(2 * self._capacity)           # 2-4. allocate bigger, copy, swap refs
        self._A[self._n] = obj                         # 5. store new element
        self._n += 1                                   # 6. update size

    def _resize(self, c):
        B = self._make_array(c)                        # new larger array
        for k in range(self._n):                       # copy existing references
            B[k] = self._A[k]
        self._A = B                                    # old array becomes garbage
        self._capacity = c

    def insert(self, k, value):
        if self._n == self._capacity:
            self._resize(2 * self._capacity)
        for j in range(self._n, k, -1):                # shift right: O(n - k)
            self._A[j] = self._A[j - 1]
        self._A[k] = value
        self._n += 1

    def pop(self):
        if self._n == 0:
            raise IndexError("pop from empty array")
        v = self._A[self._n - 1]
        self._A[self._n - 1] = None
        self._n -= 1
        return v


def dynamic_array_demo():
    d = DynamicArray()
    last_cap = d._capacity
    print("size  capacity")
    for i in range(1, 18):
        d.append(i * 10)
        if d._capacity != last_cap or i == 1:
            print(f"{len(d):>4}  {d._capacity:>8}   <- resized")
            last_cap = d._capacity
    print("elements:", [d[i] for i in range(len(d))])

    lst, prev = [], None
    print("\nCPython list over-allocation (sys.getsizeof):")
    for i in range(30):
        lst.append(i)
        s = sys.getsizeof(lst)
        if s != prev:
            print(f"  len={len(lst):>2}  bytes={s}")
            prev = s


# ---- list / tuple / str ---------------------------------------------------
def sequence_types_demo():
    lst, tup, s = [1, 2, 3], (1, 2, 3), "abc"
    lst[0] = 100
    print("list mutated:", lst)
    for name, obj in (("tuple", tup), ("str", s)):
        try:
            obj[0] = 100
        except TypeError as e:
            print(f"{name} item assignment fails -> {e}")
    print("sizeof list/tuple (3 ints):", sys.getsizeof([1, 2, 3]), sys.getsizeof((1, 2, 3)))
    print("tuple of immutables is hashable ->", hash((1, 2, 3)) is not None)
    try:
        hash([1, 2, 3])
    except TypeError as e:
        print("list is not hashable ->", e)


# ---- 2-D dataset with nested lists ---------------------------------------
def nested_list_demo():
    rows, cols = 3, 4
    grid = [[r * cols + c for c in range(cols)] for r in range(rows)]   # correct creation
    print("grid:", *grid, sep="\n  ")
    print("row access grid[1]            :", grid[1], " -> O(1) (reference), copy row[:] is O(cols)")
    print("column traversal [r[2] for r] :", [r[2] for r in grid], " -> O(rows)")
    print("element grid[2][3]            :", grid[2][3], " -> O(1)")
    print("sum of all elements           :", sum(sum(r) for r in grid), " -> O(rows*cols)")

    bad = [[0] * cols] * rows                    # common bug: same row object repeated
    bad[0][0] = 7
    print("\nBug demo [[0]*c]*r -> modifying one cell changes every row:", bad)
    transposed = [list(col) for col in zip(*grid)]
    print("transpose:", transposed, " -> O(rows*cols)")


# ---- Empirical complexity table for list operations ----------------------
def complexity_benchmark():
    import timeit
    print("\nEmpirical check (microseconds per op, list of n elements):")
    print(f"{'op':<16}{'n=10^4':>12}{'n=10^5':>12}")
    ops = {
        "L[k] index":      "L[5000]",
        "len(L)":          "len(L)",
        "x in L":          "-1 in L",
        "L.append(1)":     "L.append(1)",
        "L.insert(0,1)":   "L.insert(0, 1)",
        "L.pop()":         "L.append(1); L.pop()",
        "L.pop(0)":        "L.append(1); L.pop(0)",
        "L[:] slice":      "L[:]",
    }
    for name, stmt in ops.items():
        row = []
        for n in (10**4, 10**5):
            t = timeit.timeit(stmt, setup=f"L=list(range({n}))", number=200) / 200
            row.append(t * 1e6)
        print(f"{name:<16}{row[0]:>12.3f}{row[1]:>12.3f}")


def part_b_main():
    print("== Shallow vs deep copy =="); copy_demo()
    print("\n== Dynamic array =="); dynamic_array_demo()
    print("\n== list / tuple / str =="); sequence_types_demo()
    print("\n== Nested lists as 2-D data =="); nested_list_demo()
    complexity_benchmark()


##############################################################################
# PART C - Stacks, Queues and Deques
##############################################################################
# Part C - Stacks, Queues and Deques (coding questions)
# Name: Aditya Raj | Roll No: 25BEC007
# Run: python stacks_queues_deques.py



class Empty(Exception):
    """Raised when accessing an element from an empty container."""


# ============================= STACK ======================================
class ArrayStack:
    """LIFO stack backed by a Python list.
    push O(1)*, pop O(1)*, top O(1), is_empty O(1), len O(1)   (*amortised; worst-case O(n) on resize)
    Space: O(n)."""

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, e):
        self._data.append(e)

    def top(self):
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data.pop()


def reverse_with_stack(seq, trace=False):
    S = ArrayStack()
    for x in seq:
        S.push(x)
        if trace:
            print(f"  push {x!r:>4} -> size {len(S)}")
    out = []
    while not S.is_empty():
        x = S.pop()
        out.append(x)
        if trace:
            print(f"  pop  {x!r:>4} -> output {out}")
    return out


def is_matched(expr):
    """Delimiter matching that respects ORDER (uses a stack)."""
    lefts, rights = "({[", ")}]"
    S = ArrayStack()
    for c in expr:
        if c in lefts:
            S.push(c)
        elif c in rights:
            if S.is_empty() or rights.index(c) != lefts.index(S.pop()):
                return False
    return S.is_empty()


def counts_balanced(expr):
    """Naive count-only check (ignores order) - gives wrong answers, for comparison."""
    return all(expr.count(a) == expr.count(b) for a, b in ("()", "{}", "[]"))


# ============================= QUEUE ======================================
class ArrayQueue:
    """Circular-array queue using data, size and front.
    next insertion index = (front + size) % len(data)
    next front           = (front + 1)    % len(data)
    All operations O(1) amortised."""
    DEFAULT_CAPACITY = 4

    def __init__(self):
        self._data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Empty("Queue is empty")
        return self._data[self._front]

    def dequeue(self):
        if self.is_empty():
            raise Empty("Queue is empty")
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer

    def enqueue(self, e):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1

    def _resize(self, cap):
        old = self._data
        self._data = [None] * cap
        walk = self._front
        for k in range(self._size):          # realign so front becomes index 0
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0


class ListQueue:
    """Inefficient queue: dequeue uses list.pop(0) -> O(n) shift of all remaining items.
    Dequeuing all n items costs (n-1)+(n-2)+...+0 = n(n-1)/2 = O(n^2)."""

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return not self._data

    def enqueue(self, e):
        self._data.append(e)

    def dequeue(self):
        if not self._data:
            raise Empty("Queue is empty")
        return self._data.pop(0)


# ============================= DEQUE ======================================
class ArrayDeque:
    """Circular-array double-ended queue. All operations O(1) amortised."""

    def __init__(self, capacity=4):
        self._data = [None] * capacity
        self._size = 0
        self._front = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._data[self._front]

    def last(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        return self._data[(self._front + self._size - 1) % len(self._data)]

    def add_first(self, e):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        self._front = (self._front - 1) % len(self._data)    # step BACK one slot
        self._data[self._front] = e
        self._size += 1

    def add_last(self, e):
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        back = (self._front + self._size) % len(self._data)
        self._data[back] = e
        self._size += 1

    def delete_first(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        ans = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return ans

    def delete_last(self):
        if self.is_empty():
            raise Empty("Deque is empty")
        back = (self._front + self._size - 1) % len(self._data)
        ans = self._data[back]
        self._data[back] = None
        self._size -= 1
        return ans

    def _resize(self, cap):
        old, walk = self._data, self._front
        self._data = [None] * cap
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (walk + 1) % len(old)
        self._front = 0

    def to_list(self):
        return [self._data[(self._front + i) % len(self._data)] for i in range(self._size)]


# ====================== Application selections ============================
class BrowserHistory:
    """Two stacks: back-stack and forward-stack (LIFO matches 'most recent page first')."""

    def __init__(self, home):
        self.current, self.back, self.fwd = home, ArrayStack(), ArrayStack()

    def visit(self, url):
        self.back.push(self.current)
        self.current = url
        self.fwd = ArrayStack()                  # new visit clears forward history

    def go_back(self):
        if not self.back.is_empty():
            self.fwd.push(self.current)
            self.current = self.back.pop()
        return self.current

    def go_forward(self):
        if not self.fwd.is_empty():
            self.back.push(self.current)
            self.current = self.fwd.pop()
        return self.current


def round_robin(tasks, quantum):
    """Task scheduling with a queue (FIFO fairness). tasks: {name: remaining_time}."""
    Q = ArrayQueue()
    for name, t in tasks.items():
        Q.enqueue((name, t))
    timeline = []
    while not Q.is_empty():
        name, t = Q.dequeue()
        run = min(quantum, t)
        timeline.append((name, run))
        if t - run > 0:
            Q.enqueue((name, t - run))
    return timeline


def is_palindrome(s):
    """Deque: compare/remove from both ends."""
    D = ArrayDeque()
    for ch in s.lower():
        if ch.isalnum():
            D.add_last(ch)
    while len(D) > 1:
        if D.delete_first() != D.delete_last():
            return False
    return True


def sliding_window_max(nums, k):
    """Monotonic deque of indices - O(n) overall (each index enters/leaves once)."""
    D, out = deque(), []
    for i, x in enumerate(nums):
        while D and nums[D[-1]] <= x:
            D.pop()
        D.append(i)
        if D[0] <= i - k:
            D.popleft()
        if i >= k - 1:
            out.append(nums[D[0]])
    return out


# ============================ Benchmark ===================================
def bench_ends(n=20000):
    def run(make, front_insert, front_delete):
        c = make()
        t0 = time.perf_counter()
        for i in range(n):
            front_insert(c, i)
        for _ in range(n):
            front_delete(c)
        return time.perf_counter() - t0

    def mk_ad(): return ArrayDeque()
    res = {
        "list  (insert(0)/pop(0))": run(list, lambda c, x: c.insert(0, x), lambda c: c.pop(0)),
        "list  (append/pop)":      run(list, lambda c, x: c.append(x), lambda c: c.pop()),
        "ArrayDeque (circular)":   run(mk_ad, lambda c, x: c.add_first(x), lambda c: c.delete_first()),
        "collections.deque":       run(deque, lambda c, x: c.appendleft(x), lambda c: c.popleft()),
    }
    print(f"Insert then delete {n} items at the FRONT (seconds):")
    for k, v in res.items():
        print(f"  {k:<26}{v:.4f}")


def part_c_main():
    print("== Stack ==")
    S = ArrayStack()
    for x in (5, 3, 8):
        S.push(x)
    print("top:", S.top(), "len:", len(S), "pop:", S.pop(), S.pop(), S.pop())
    for op in (S.pop, S.top):
        try:
            op()
        except Empty as e:
            print(f"{op.__name__}() on empty ->", type(e).__name__, "-", e)

    print("\n== Reversal with a stack: trace for [1,2,3,4] ==")
    print("result:", reverse_with_stack([1, 2, 3, 4], trace=True))

    print("\n== Delimiter matching: stack vs counting ==")
    for e in ("([]{})", "([)]", ")(", "{[()]}(", "a(b)c"):
        print(f"{e:<10} stack={is_matched(e)!s:<6} counting-only={counts_balanced(e)}")

    print("\n== Circular ArrayQueue ==")
    Q = ArrayQueue()
    for i in range(1, 6):
        Q.enqueue(i)
    print("dequeued:", Q.dequeue(), Q.dequeue(), "first:", Q.first(), "len:", len(Q))
    for i in (6, 7, 8):                      # forces wrap-around and resize
        Q.enqueue(i)
    print("drain:", [Q.dequeue() for _ in range(len(Q))])
    try:
        Q.dequeue()
    except Empty as e:
        print("dequeue on empty ->", e)

    print("\n== ArrayDeque ==")
    D = ArrayDeque()
    D.add_last(1); D.add_last(2); D.add_first(0); D.add_first(-1); D.add_last(3)
    print("deque:", D.to_list(), "first:", D.first(), "last:", D.last())
    print("delete_first:", D.delete_first(), "delete_last:", D.delete_last(), "->", D.to_list())

    print("\n== list.pop(0) vs circular queue ==")
    for n in (2000, 4000, 8000, 16000):
        res = []
        for cls in (ListQueue, ArrayQueue):
            q = cls()
            for i in range(n):
                q.enqueue(i)
            t0 = time.perf_counter()
            while not q.is_empty():
                q.dequeue()
            res.append(time.perf_counter() - t0)
        print(f"n={n:>6}  ListQueue={res[0]:.4f}s  ArrayQueue={res[1]:.4f}s")

    print("\n== Deque end-operation comparison ==")
    bench_ends()

    print("\n== Applications ==")
    b = BrowserHistory("home")
    b.visit("a.com"); b.visit("b.com"); b.visit("c.com")
    print("back:", b.go_back(), b.go_back(), "| forward:", b.go_forward(), "| visit d.com:", (b.visit("d.com"), b.current)[1])
    print("round robin (q=2):", round_robin({"A": 5, "B": 3, "C": 1}, 2))
    for s in ("A man, a plan, a canal: Panama", "racecar", "hello", ""):
        print(f"palindrome({s!r}) = {is_palindrome(s)}")
    print("sliding window max [1,3,-1,-3,5,3,6,7], k=3 ->", sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))

    # self-checks
    assert is_matched("([]{})") and not is_matched("([)]") and not is_matched(")(")
    assert sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    print("\nAll assertions passed.")


##############################################################################
# PART D - Linked Lists
##############################################################################
# Part D - Linked Lists (coding questions)
# Name: Aditya Raj | Roll No: 25BEC007
# Run: python linked_lists.py

# (Empty exception shared with Part C)


# ======================= Singly linked list ===============================
class _Node:
    """element = stored object, next = reference to following node (None at the tail)."""
    __slots__ = "element", "next"

    def __init__(self, element, next=None):
        self.element = element
        self.next = next


class SinglyLinkedList:
    """Maintains head, tail and size.  Empty: head=tail=None, size=0.  Singleton: head is tail."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def insert_first(self, e):                      # O(1)
        """Pre: none.  new.next = head; head = new; if list was empty, tail = new."""
        new = _Node(e, self.head)
        self.head = new
        if self.tail is None:
            self.tail = new
        self.size += 1

    def insert_last(self, e):                       # O(1) thanks to tail
        """Pre: none.  new.next = None; tail.next = new (if non-empty else head = new); tail = new."""
        new = _Node(e)
        if self.tail is None:
            self.head = new
        else:
            self.tail.next = new
        self.tail = new
        self.size += 1

    def delete_first(self):                         # O(1)
        """Pre: list not empty.  head = head.next; if list becomes empty, tail = None."""
        if self.is_empty():
            raise Empty("list is empty")
        e = self.head.element
        self.head = self.head.next
        self.size -= 1
        if self.size == 0:
            self.tail = None
        return e

    def traverse(self):                             # O(n)
        cur = self.head
        while cur is not None:
            yield cur.element
            cur = cur.next

    def __iter__(self):
        return self.traverse()

    def __repr__(self):
        return " -> ".join(map(str, self)) + " -> None" if self.size else "(empty)"

    def reverse(self):                              # bonus: in-place reversal, O(n)
        prev, cur = None, self.head
        self.tail = self.head
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        self.head = prev


# ======================= Doubly linked list ===============================
class _DNode:
    __slots__ = "element", "prev", "next"

    def __init__(self, element, prev, next):
        self.element, self.prev, self.next = element, prev, next


class DoublyLinkedList:
    """Uses header/trailer sentinels so insert/delete never special-case the ends."""

    def __init__(self):
        self._header = _DNode(None, None, None)
        self._trailer = _DNode(None, None, None)
        self._header.next = self._trailer
        self._trailer.prev = self._header
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def _insert_between(self, e, predecessor, successor):
        """new.prev = pred; new.next = succ; pred.next = new; succ.prev = new."""
        new = _DNode(e, predecessor, successor)
        predecessor.next = new
        successor.prev = new
        self._size += 1
        return new

    def _delete_node(self, node):
        """node.prev.next = node.next; node.next.prev = node.prev; clear node's references."""
        pred, succ = node.prev, node.next
        pred.next = succ
        succ.prev = pred
        self._size -= 1
        e = node.element
        node.prev = node.next = node.element = None
        return e

    def add_first(self, e):
        return self._insert_between(e, self._header, self._header.next)

    def add_last(self, e):
        return self._insert_between(e, self._trailer.prev, self._trailer)

    def delete_first(self):
        if self.is_empty():
            raise Empty("list is empty")
        return self._delete_node(self._header.next)

    def delete_last(self):
        if self.is_empty():
            raise Empty("list is empty")
        return self._delete_node(self._trailer.prev)

    def __iter__(self):
        cur = self._header.next
        while cur is not self._trailer:
            yield cur.element
            cur = cur.next

    def __repr__(self):
        return "<-> ".join(map(str, self)) if self._size else "(empty)"


# ======================= Positional list ==================================
class PositionalList(DoublyLinkedList):
    """Positions are stable handles: they stay valid when other elements are inserted/removed,
    unlike integer indices which shift."""

    class Position:
        def __init__(self, container, node):
            self._container, self._node = container, node

        def element(self):
            return self._node.element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            return not (self == other)

    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError("p must be proper Position type")
        if p._container is not self:
            raise ValueError("p does not belong to this container")
        if p._node.next is None:
            raise ValueError("p is no longer valid")
        return p._node

    def _make_position(self, node):
        if node is self._header or node is self._trailer:
            return None
        return self.Position(self, node)

    def first(self):
        return self._make_position(self._header.next)

    def last(self):
        return self._make_position(self._trailer.prev)

    def before(self, p):
        return self._make_position(self._validate(p).prev)

    def after(self, p):
        return self._make_position(self._validate(p).next)

    def __iter__(self):
        cur = self.first()
        while cur is not None:
            yield cur.element()
            cur = self.after(cur)

    def _insert_between(self, e, predecessor, successor):
        return self._make_position(super()._insert_between(e, predecessor, successor))

    def add_first(self, e):
        return self._insert_between(e, self._header, self._header.next)

    def add_last(self, e):
        return self._insert_between(e, self._trailer.prev, self._trailer)

    def add_before(self, p, e):
        n = self._validate(p)
        return self._insert_between(e, n.prev, n)

    def add_after(self, p, e):
        n = self._validate(p)
        return self._insert_between(e, n, n.next)

    def delete(self, p):
        return self._delete_node(self._validate(p))

    def replace(self, p, e):
        n = self._validate(p)
        old, n.element = n.element, e
        return old


# ======================= Favorites list ===================================
class FavoritesList:
    """Stored item fields: _Item(value, count).  List is kept sorted by count (descending).
    access(e): count += 1, then move item toward the front past all items with smaller count.
    remove(e): delete the item.   top(k): first k items (highest counts)."""

    class _Item:
        __slots__ = "_value", "_count"

        def __init__(self, e):
            self._value, self._count = e, 0

    def __init__(self):
        self._data = PositionalList()

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return self._data.is_empty()

    def _find_position(self, e):
        walk = self._data.first()
        while walk is not None and walk.element()._value != e:
            walk = self._data.after(walk)
        return walk

    def _move_up(self, p):
        if p != self._data.first():
            cnt = p.element()._count
            walk = self._data.before(p)
            if cnt > walk.element()._count:
                while walk != self._data.first() and cnt > self._data.before(walk).element()._count:
                    walk = self._data.before(walk)
                self._data.add_before(walk, self._data.delete(p))

    def access(self, e):
        p = self._find_position(e)
        if p is None:
            p = self._data.add_last(self._Item(e))
        p.element()._count += 1
        self._move_up(p)

    def remove(self, e):
        p = self._find_position(e)
        if p is not None:
            self._data.delete(p)

    def top(self, k):
        if not 1 <= k <= len(self):
            raise ValueError("Illegal value for k")
        walk = self._data.first()
        for _ in range(k):
            item = walk.element()
            yield item._value, item._count
            walk = self._data.after(walk)


# ============================== demo ======================================
def part_d_main():
    print("== Singly linked list ==")
    L = SinglyLinkedList()
    print("empty:", L, "| len", len(L), "| head/tail:", L.head, L.tail)
    L.insert_first(10)
    print("singleton:", L, "| head is tail:", L.head is L.tail)
    L.insert_first(5); L.insert_last(20); L.insert_last(30)
    print("multi:", L, "| len", len(L), "| head:", L.head.element, "tail:", L.tail.element)
    print("delete_first ->", L.delete_first(), "|", L)
    L.reverse(); print("reversed:", L, "| tail:", L.tail.element)
    while not L.is_empty():
        L.delete_first()
    print("after emptying: head/tail =", L.head, L.tail)
    try:
        L.delete_first()
    except Empty as e:
        print("delete_first on empty ->", e)

    print("\n== Doubly linked list ==")
    D = DoublyLinkedList()
    D.add_last(1); D.add_last(3)
    mid = D._insert_between(2, D._header.next, D._header.next.next)   # between 1 and 3
    print("insert between 1 and 3:", D)
    D._delete_node(mid); print("delete middle node:  ", D)
    D.add_first(0); print("add_first(0):", D)
    print("delete_last ->", D.delete_last(), "|", D)

    print("\n== Positional list ==")
    P = PositionalList()
    a = P.add_last("A"); c = P.add_last("C")
    b = P.add_after(a, "B")
    P.add_first("Z")                       # indices of A, B, C all shift ...
    print("list:", list(P), "| position b still refers to:", b.element())
    P.delete(a)
    print("after deleting A:", list(P), "| b still valid ->", b.element(), "| before(b) =", P.before(b).element())
    try:
        P.after(a)
    except ValueError as e:
        print("using deleted position ->", e)

    print("\n== Favorites list ==")
    F = FavoritesList()
    for page in "home about home blog home blog contact home blog about".split():
        F.access(page)
    print("top(3):", list(F.top(3)))
    F.remove("home")
    print("after remove('home'), top(3):", list(F.top(3)))


if __name__ == "__main__":
    runs = {"A": part_a_main, "B": part_b_main, "C": part_c_main, "D": part_d_main}
    chosen = [a.upper() for a in sys.argv[1:] if a.upper() in runs] or list(runs)
    for k in chosen:
        print("\n" + "=" * 70 + f"\nPART {k}\n" + "=" * 70)
        runs[k]()
