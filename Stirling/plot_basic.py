# -*- coding: utf-8 -*-
"""
绘制基础 Stirling 公式的比值随 n 增大而逼近 1 的过程。

左图：比值本身随 n 的变化（靠近 1）
右图：与 1 的偏差随 n 的变化（对数刻度，呈 1/(12n) 规律）
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpmath import mp, mpf, sqrt, exp, log, pi, factorial

mp.dps = 500


def stirling_basic(n):
    n = mpf(n)
    return sqrt(2 * pi * n) * exp(n * (log(n) - 1))


plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 采样点
ns = [1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 80, 100, 200, 500,
      1000, 2000, 5000, 10000, 20000, 50000, 100000]

ratios = []
devs = []
for n in ns:
    real = factorial(n)
    ratio = stirling_basic(n) / real
    ratios.append(float(ratio))
    devs.append(abs(float(ratio - 1)))

fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))

# ===== 图1：比值随 n 逼近 1 =====
ax = axes[0]
ax.semilogx(ns, ratios, "o-", color="#2c7fb8", markersize=5, linewidth=1.6,
            label="近似值 / 真实值")
ax.axhline(1.0, color="green", linestyle="--", linewidth=1.5,
           label="目标值 1")
ax.set_xlabel("n  (对数刻度)", fontsize=12)
ax.set_ylabel("近似值 / 真实值", fontsize=12)
ax.set_title("图1  比值随 n 增大而逼近 1", fontsize=13)
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=10)

# ===== 图2：偏差随 n 下降（对数-对数）=====
ax2 = axes[1]
ax2.loglog(ns, devs, "s-", color="#d95f02", markersize=5, linewidth=1.6,
           label="近似值/真实值 与 1 的偏差")
# 叠加理论曲线 1/(12n)
theory = [1.0 / (12 * n) for n in ns]
ax2.loglog(ns, theory, "--", color="green", linewidth=1.5,
           label="理论误差 1/(12n)")
ax2.set_xlabel("n  (对数刻度)", fontsize=12)
ax2.set_ylabel("与 1 的偏差 (对数刻度)", fontsize=12)
ax2.tick_params(axis="both", which="both", labelsize=10)
ax2.set_title("图2  偏差随 n 下降，符合 1/(12n) 规律", fontsize=13)
ax2.grid(True, which="both", alpha=0.3)
ax2.legend(fontsize=10)

plt.tight_layout()
plt.savefig("stirling_basic_plot.png", dpi=150, bbox_inches="tight")
print("图已保存: stirling_basic_plot.png")
