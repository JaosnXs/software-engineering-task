# -*- coding: utf-8 -*-
"""
Stirling 公式（基础版）精度验证。

要求：只使用基础公式，不添加任何修正项，
      通过不断增大 n 的值，使「近似值 / 真实值」的比值逼近 1。

基础公式：
    n! ~ sqrt(2*pi*n) * (n/e)^n

其相对误差约为 1/(12n)，因此 n 越大，比值越接近 1。
"""

from mpmath import mp, mpf, sqrt, exp, log, pi, factorial

# 高精度计算环境：保证真实 n! 与近似值都能精确比较
mp.dps = 500


def stirling_basic(n):
    """基础 Stirling 公式：sqrt(2*pi*n) * (n/e)^n"""
    n = mpf(n)
    return sqrt(2 * pi * n) * exp(n * (log(n) - 1))


def main():
    print("=" * 78)
    print("基础 Stirling 公式：n! ~ sqrt(2*pi*n) * (n/e)^n")
    print("通过增大 n，使 近似值/真实值 逼近 1")
    print("=" * 78)
    print()
    print(f"{'n':>8} {'近似值/真实值':>30} {'与 1 的偏差':>16}")
    print("-" * 78)

    # 逐步增大 n，观察比值趋近 1 的过程
    test_ns = [1, 2, 5, 10, 20, 50, 100, 200, 500,
               1000, 2000, 5000, 10000, 20000, 50000, 100000]

    for n in test_ns:
        real = factorial(n)
        approx = stirling_basic(n)
        ratio = approx / real
        dev = abs(ratio - 1)
        print(f"{n:>8} {mp.nstr(ratio, 26):>30} {mp.nstr(dev, 4):>16}")

    print()
    print("=" * 78)
    print("结论")
    print("=" * 78)
    print("基础公式的相对误差约为 1/(12n)：")
    print("  n=100    时偏差约 8e-4")
    print("  n=1000   时偏差约 8e-5")
    print("  n=10000  时偏差约 8e-6")
    print("  n=100000 时偏差约 8e-7")
    print()
    print("可见随着 n 增大，比值单调趋近 1，符合 1/(12n) 的误差规律。")
    print("=" * 78)


if __name__ == "__main__":
    main()
