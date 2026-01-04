import argparse
import time
import sys
import numpy as np

def benchmark_cpu(duration=10):
    """
    Benchmark CPU by performing as many floating-point operations as possible in the given duration.
    Returns operations per second.
    """
    operations = 0
    start_time = time.time()
    end_time = start_time + duration
    a = 1.0
    b = 2.0
    while time.time() < end_time:
        for _ in range(1000):  # Batch operations to reduce loop overhead
            a = a * b + a / b - a + b
        operations += 1000 * 4  # Each inner loop has 4 operations: *, +, /, -
    elapsed = time.time() - start_time
    ops_per_sec = operations / elapsed
    print(f"CPU Benchmark: {ops_per_sec:.2e} operations per second over {elapsed:.2f} seconds.")
    return ops_per_sec

def benchmark_ram(duration=10):
    """
    Benchmark RAM by copying large arrays repeatedly for the given duration.
    Measures memory operations in terms of bytes copied per second, converted to approximate operations.
    Assuming each byte copy is roughly one operation.
    """
    # Create large arrays: 100 MB each
    size = 100 * 1024 * 1024 // 8  # 100 MB in doubles (8 bytes each)
    src = np.random.rand(size)
    dst = np.zeros(size)
    
    bytes_copied = 0
    start_time = time.time()
    end_time = start_time + duration
    while time.time() < end_time:
        np.copyto(dst, src)
        bytes_copied += size * 8  # Bytes copied per operation
    elapsed = time.time() - start_time
    bytes_per_sec = bytes_copied / elapsed
    # Approximate operations per second (assuming 1 operation per byte copied)
    ops_per_sec = bytes_per_sec
    print(f"RAM Benchmark: {ops_per_sec:.2e} operations (bytes copied) per second over {elapsed:.2f} seconds.")
    return ops_per_sec

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple system benchmark")
    parser.add_argument("--mode", choices=["cpu", "ram"], default="cpu", help="Which benchmark to use (default is 'cpu')")
    parser.add_argument("--duration", type=float, default=10.0, help="Duration of the benchmark (default is '10.0' seconds)")
    parser.add_argument("--size", type=int, default=100, help="Array size in MB for RAM benchmark (default is '100')")

    args = parser.parse_args()

    print(f"Running benchmark '{args.mode}' for '{args.duration}' seconds\n")
    
    if args.mode == 'cpu':
        benchmark_cpu(args.duration)

    else:
        benchmark_ram(args.duration)
