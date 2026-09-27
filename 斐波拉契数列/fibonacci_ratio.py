# -*- coding: utf-8 -*-
"""
题目：计算斐波那契数列，求「前项比后项」的比值首次落入
      0.61840 ~ 0.61860 区间时，对应的是第几项。

比值定义：ratio(n) = F(n-1) / F(n)
该比值在极限 1/phi = 0.6180339887... 两侧上下震荡收敛，
因此会反复穿越目标区间，需要往后多推导若干项才能找到。
"""

from decimal import Decimal, getcontext

# 提高精度，避免浮点误差干扰边界判断
getcontext().prec = 60

LOW = Decimal("0.61840")
HIGH = Decimal("0.61860")


def build_fib(limit):
    """生成斐波那契数列 F(1)=1, F(2)=1, ...，返回 list，下标 0 对应 F(1)。"""
    seq = [1, 1]
    while len(seq) < limit:
        seq.append(seq[-1] + seq[-2])
    return seq


def ratio_of(prev, curr):
    """前项 / 后项"""
    return Decimal(prev) / Decimal(curr)


def main():
    print("=" * 70)
    print("目标区间: [0.61840, 0.61860]     比值 = F(n-1) / F(n)")
    print("=" * 70)
    print()

    N = 120
    seq = build_fib(N)

    # 打印各项比值，标注是否在区间内，并显示震荡方向
    print(f"{'n':>4} {'F(n-1)':>28} {'F(n)':>28} {'ratio':>16}  标记")
    print("-" * 90)

    first_hit = None
    prev_ratio = None

    for n in range(2, N + 1):
        p, c = seq[n - 2], seq[n - 1]
        r = ratio_of(p, c)

        in_range = LOW <= r <= HIGH
        if in_range:
            mark = "<== 命中"
        else:
            mark = ""

        # 只打印前 20 项 + 所有命中项附近的项，避免刷屏
        if n <= 20 or in_range or (first_hit and n <= first_hit[0] + 2):
            print(f"{n:>4} {p:>28} {c:>28} {r:>16.10f}  {mark}")

        if in_range and first_hit is None:
            first_hit = (n, p, c, r)

        prev_ratio = r

    print()
    print("=" * 70)
    if first_hit:
        n, p, c, r = first_hit
        print(f"首次进入区间发生在第 {n} 项")
        print(f"  F({n-1}) = {p}")
        print(f"  F({n})   = {c}")
        print(f"  F({n-1}) / F({n}) = {r:.12f}")
        print(f"  区间 [0.61840, 0.61860] 内，判定通过。")
    else:
        print("在给定范围内没有找到满足条件的项。")
    print("=" * 70)


if __name__ == "__main__":
    main()
