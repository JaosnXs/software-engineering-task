# -*- coding: utf-8 -*-
"""
绘制斐波那契相邻项比值 F(n-1)/F(n) 随项数 n 的变化曲线，
并标出目标区间 [0.61840, 0.61860] 与极限值 1/phi。

纵轴做了细化：收紧范围 + 加密刻度 + 显示小数点后 5 位，
以便观察震荡收敛的细节。
"""

import matplotlib
matplotlib.use("Agg")  # 无界面环境也能出图
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from decimal import Decimal, getcontext

getcontext().prec = 60

LOW = Decimal("0.61840")
HIGH = Decimal("0.61860")
PHI_INV = Decimal("0.6180339887498948482")  # 1/phi 极限值

# ---------- 计算数据 ----------
N = 40
seq = [1, 1]
while len(seq) < N:
    seq.append(seq[-1] + seq[-2])

ns = list(range(2, N + 1))
ratios = [float(Decimal(seq[n - 2]) / Decimal(seq[n - 1])) for n in ns]

# 找出命中项
hits = [(n, r) for n, r in zip(ns, ratios) if float(LOW) <= r <= float(HIGH)]

# 中文字体设置
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ---------- 绘图 ----------
fig, axes = plt.subplots(1, 3, figsize=(21, 6.5))


def style_axis(ax, title, ymin, ymax, ystep):
    """统一设置纵轴范围、刻度密度与格式。"""
    ax.set_ylim(ymin, ymax)
    ax.yaxis.set_major_locator(MultipleLocator(ystep))
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.5f"))
    # 加密次刻度，让纵轴更精细
    ax.yaxis.set_minor_locator(MultipleLocator(ystep / 5))
    ax.tick_params(axis="y", which="major", labelsize=9)
    ax.tick_params(axis="y", which="minor", length=3)
    ax.grid(True, which="major", alpha=0.35)
    ax.grid(True, which="minor", alpha=0.15, linestyle=":")
    ax.set_xlabel("n  (项数)", fontsize=12)
    ax.set_ylabel("F(n-1) / F(n)", fontsize=12)
    ax.set_title(title, fontsize=13)


# ===== 图1：整体趋势（纵轴 0.49 ~ 1.01）=====
ax = axes[0]
ax.plot(ns, ratios, "o-", color="#2c7fb8", markersize=5,
        linewidth=1.5, label="F(n-1) / F(n)")
ax.axhspan(float(LOW), float(HIGH), color="#f03b20", alpha=0.25,
           label="目标区间 [0.61840, 0.61860]")
ax.axhline(float(PHI_INV), color="green", linestyle="--", linewidth=1.5,
           label="极限 1/phi = 0.6180339")
style_axis(ax, "图1  整体趋势（震荡收敛）", 0.49, 1.01, 0.05)
ax.legend(fontsize=9, loc="upper right")

# ===== 图2：纵轴细化（0.6170 ~ 0.6200）=====
ax2 = axes[1]
ax2.plot(ns, ratios, "o-", color="#2c7fb8", markersize=5,
         linewidth=1.5, label="F(n-1) / F(n)")
ax2.axhspan(float(LOW), float(HIGH), color="#f03b20", alpha=0.25,
            label="目标区间 [0.61840, 0.61860]")
ax2.axhline(float(PHI_INV), color="green", linestyle="--", linewidth=1.5,
            label="极限 1/phi = 0.6180339")
style_axis(ax2, "图2  纵轴细化：看清能否进入区间", 0.6170, 0.6200, 0.0005)
ax2.legend(fontsize=9, loc="upper right")

# 标注 n=8、n=9 两个跨越区间的关键点
for n, dy in ((8, 0.00035), (9, -0.00045)):
    r = ratios[ns.index(n)]
    ax2.annotate(f"n={n}\n{r:.6f}", xy=(n, r),
                 xytext=(n + 1.2, r + dy),
                 fontsize=9, color="darkred",
                 arrowprops=dict(arrowstyle="->", color="darkred"))

# ===== 图3：极限附近极细放大（0.61790 ~ 0.61820）=====
ax3 = axes[2]
ax3.plot(ns, ratios, "o-", color="#2c7fb8", markersize=5,
         linewidth=1.5, label="F(n-1) / F(n)")
ax3.axhspan(float(LOW), float(HIGH), color="#f03b20", alpha=0.25,
            label="目标区间 [0.61840, 0.61860]")
ax3.axhline(float(PHI_INV), color="green", linestyle="--", linewidth=1.5,
            label="极限 1/phi = 0.6180339")
style_axis(ax3, "图3  极限附近极细放大（n>=10 的窄带）", 0.61790, 0.61820, 0.0001)
ax3.legend(fontsize=9, loc="upper right")

# 标注 n>=10 的震荡上沿，说明够不到区间下界
ax3.annotate("n>=10 全部落在此窄带内\n上沿 0.61818 < 区间下界 0.61840",
             xy=(15, 0.61818), xytext=(18, 0.61810),
             fontsize=9, color="darkred",
             arrowprops=dict(arrowstyle="->", color="darkred"))

plt.tight_layout()
plt.savefig("fib_ratio_plot.png", dpi=150, bbox_inches="tight")
print("图已保存: fib_ratio_plot.png")
print(f"命中项数量: {len(hits)}")
if hits:
    for n, r in hits:
        print(f"  n={n}, ratio={r:.10f}")
else:
    print("  区间内无命中项")
