import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False
import numpy as np
import matplotlib.pyplot as plt

# 模拟参数
S0 = 772.68              # 初始黄金价格（2025年6月10日Au99.99收盘价）
r = 0.01655              # 无风险利率
sigma = 0.1437           # 年化波动率（14.37%）
T = 183 / 252            # 模拟周期（183天，按252个交易日年化）
N = 183                  # 时间步数（每天一个点）
dt = T / N
n_paths = 20000          # 要显示的模拟路径数量（可设为20000用于VaR）

# 模拟路径
np.random.seed(0)
Z = np.random.randn(n_paths, N)
S = np.zeros((n_paths, N+1))
S[:, 0] = S0

for t in range(1, N+1):
    S[:, t] = S[:, t-1] * np.exp((r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, t-1])

# 绘图
plt.figure(figsize=(10, 6))
for i in range(min(n_paths, 100)):
    plt.plot(S[i], lw=0.5)

plt.title("蒙特卡洛模拟黄金价格路径（展示前100条）", fontsize=14)
plt.xlabel("交易日", fontsize=12)
plt.ylabel("价格（元/克）", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# 绘制终点价格频数直方图
plt.figure(figsize=(8, 5))
plt.hist(S[:, -1], bins=50, color='skyblue', edgecolor='black')
plt.title("模拟期末黄金价格分布直方图", fontsize=14)
plt.xlabel("期末价格（元/克）", fontsize=12)
plt.ylabel("频数", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()