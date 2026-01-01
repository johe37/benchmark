import argparse
import multiprocessing as mp
import os
import tempfile
import time
import math
import sys

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


def timer(fn):
    start = time.perf_counter()
    result = fn()
    return time.perf_counter() - start, result


def cpu_single(n):
    x = 0.0
    for i in range(1, n):
        x += math.sqrt(i) * math.sin(i)
    return x


def cpu_worker(n):
    return cpu_single(n)


def cpu_multi(n, workers):
    with mp.Pool(workers) as p:
        p.map(cpu_worker, [n] * workers)


def memory_test(size_mb):
    size = size_mb * 1024 * 1024
    buf = bytearray(size)
    for i in range(0, size, 64):
        buf[i] = i % 256
    s = 0
    for i in range(0, size, 64):
        s += buf[i]
    return s


def disk_test(size_mb):
    size = size_mb * 1024 * 1024
    data = os.urandom(1024 * 1024)

    with tempfile.NamedTemporaryFile(delete=True) as f:
        for _ in range(size // len(data)):
            f.write(data)
        f.flush()
        f.seek(0)
        while f.read(len(data)):
            pass


def python_overhead(n):
    def inner(x):
        return x + 1

    x = 0
    for _ in range(n):
        x = inner(x)
    return x


def numpy_test(n):
    a = np.random.rand(n, n)
    b = np.random.rand(n, n)
    return np.dot(a, b)


def main():
    parser = argparse.ArgumentParser(description="Simple system benchmark")
    parser.add_argument("--size", choices=["small", "medium", "large"], default="medium")
    args = parser.parse_args()

    sizes = {
        "small": 1,
        "medium": 5,
        "large": 10
    }

    cpu_iters = sizes[args.size] * 200_000
    mem_mb = sizes[args.size] * 256
    disk_mb = sizes[args.size] * 256
    py_iters = sizes[args.size] * 5_000_000
    np_size = sizes[args.size] * 300

    print("=== Python System Benchmark ===")
    print(f"Python: {sys.version.split()[0]}")
    print(f"CPU cores: {mp.cpu_count()}")
    print(f"Benchmark size: {args.size}")
    print()

    t, _ = timer(lambda: cpu_single(cpu_iters))
    print(f"CPU single-thread: {t:.2f} s")

    t, _ = timer(lambda: cpu_multi(cpu_iters, mp.cpu_count()))
    print(f"CPU multi-thread:  {t:.2f} s")

    t, _ = timer(lambda: memory_test(mem_mb))
    print(f"Memory ({mem_mb} MB): {t:.2f} s")

    t, _ = timer(lambda: disk_test(disk_mb))
    print(f"Disk ({disk_mb} MB):   {t:.2f} s")

    t, _ = timer(lambda: python_overhead(py_iters))
    print(f"Python overhead:   {t:.2f} s")

    if HAS_NUMPY:
        t, _ = timer(lambda: numpy_test(np_size))
        print(f"NumPy ({np_size}x{np_size}): {t:.2f} s")
    else:
        print("NumPy: not installed")

    print("\nDone.")


if __name__ == "__main__":
    main()

