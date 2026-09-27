# -*- coding: utf-8 -*-
"""
Wallis 公式精度验证。

Wallis 公式：
    pi/2 = lim (n->inf) prod_{k=1}^{n} 4k^2 / (4k^2 - 1)

即部分乘积：
    P(n) = prod_{k=1}^{n} 4k^2 / (4k^2 - 1)
随着 n 增大，P(n) 趋近 pi/2。

目标：通过不断增大 n，使「P(n) / (pi/2)」的比值逼近 1。
"""

from mpmath import mp, mpf, pi

# 高精度计算环境
mp.dps = 100


def wallis_partial(n):
    """计算 Wallis 部分乘积 P(n) = prod_{k=1}^{n} 4k^2/(4k^2-1)"""
    prod = mpf(1)
    for k in range(1, n + 1):
        k = mpf(k)
        prod *= (4 * k * k) / (4 * k * k - 1)
    return prod


def main():
    print("=" * 78)
    print("Wallis 公式：pi/2 = prod 4k^2/(4k^2-1)")
    print("通过增大 n，使 部分乘积/(pi/2) 逼近 1")
    print("=" * 78)
    print()

    target = pi / 2
    print(f"目标值 pi/2 = {mp.nstr(target, 20)}")
    print()
    print(f"{'n':>10} {'P(n) / (pi/2)':>30} {'与 1 的偏差':>16}")
    print("-" * 78)

    test_ns = [1, 2, 5, 10, 20, 50, 100, 200, 500,
               1000, 2000, 5000, 10000]

    for n in test_ns:
        p = wallis_partial(n)
        ratio = p / target
        dev = abs(ratio - 1)
        print(f"{n:>10} {mp.nstr(ratio, 26):>30} {mp.nstr(dev, 4):>16}")

    print()
    print("=" * 78)
    print("结论")
    print("=" * 78)
    print("Wallis 部分乘积的偏差约为 1/(4n) 量级：")
    print("  n=100    时偏差约 2.5e-3")
    print("  n=1000   时偏差约 2.5e-4")
    print("  n=10000  时偏差约 2.5e-5")
    print("  n=100000 时偏差约 2.5e-6")
    print()
    print("可见随着 n 增大，比值单调趋近 1，")
    print("n 每增大 10 倍，偏差就缩小 10 倍。")
    print("=" * 78)


if __name__ == "__main__":
    main()
