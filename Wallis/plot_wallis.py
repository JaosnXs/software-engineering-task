# -*- coding: utf-8 -*-
"""
绘制 Wallis 公式部分乘积比值随 n 增大而逼近 1 的过程。

左图：P(n)/(pi/2) 随 n 的变化（靠近 1）
右图：与 1 的偏差随 n 的变化（对数刻度，呈 1/n 规律）

优化：只做一次累乘，在到达采样点时记录，避免重复计算。
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpmath import mp, mpf, pi

mp.dps = 50

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

target = pi / 2

# 采样点
ns = [1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 80, 100,
      200, 500, 1000, 2000]
sample_set = set(ns)
max_n = max(ns)

ratios = []
devs = []
prod = mpf(1)
for k in range(1, max_n + 1):
    kk = mpf(k)
    prod *= (4 * kk * kk) / (4 * kk * kk - 1)
    if k in sample_set:
        ratio = prod / target
        ratios.append(float(ratio))
        devs.append(abs(float(ratio - 1)))

fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))

# ===== 图1：比值随 n 逼近 1 =====
ax = axes[0]
ax.semilogx(ns, ratios, "o-", color="#2c7fb8", markersize=5, linewidth=1.6,
            label="P(n) / (pi/2)")
ax.axhline(1.0, color="green", linestyle="--", linewidth=1.5,
           label="目标值 1")
ax.set_xlabel("n  (对数刻度)", fontsize=12)
ax.set_ylabel("P(n) / (pi/2)", fontsize=12)
ax.set_title("图1  Wallis 部分乘积比值随 n 逼近 1", fontsize=13)
ax.grid(True, which="both", alpha=0.3)
ax.legend(fontsize=10)
ax.tick_params(axis="both", which="both", labelsize=10)

# ===== 图2：偏差随 n 下降（对数-对数）=====
ax2 = axes[1]
ax2.loglog(ns, devs, "s-", color="#d95f02", markersize=5, linewidth=1.6,
           label="P(n)/(pi/2) 与 1 的偏差")
# 叠加理论曲线 1/(4n)
theory = [1.0 / (4 * n) for n in ns]
ax2.loglog(ns, theory, "--", color="green", linewidth=1.5,
           label="理论误差 1/(4n)")
ax2.set_xlabel("n  (对数刻度)", fontsize=12)
ax2.set_ylabel("与 1 的偏差 (对数刻度)", fontsize=12)
ax2.set_title("图2  偏差随 n 下降，符合 1/(4n) 规律", fontsize=13)
ax2.grid(True, which="both", alpha=0.3)
ax2.legend(fontsize=10)
ax2.tick_params(axis="both", which="both", labelsize=10)

plt.tight_layout()
plt.savefig("wallis_plot.png", dpi=150, bbox_inches="tight")
print("图已保存: wallis_plot.png")
