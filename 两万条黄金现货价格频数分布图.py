import numpy as np
import matplotlib.pyplot as plt

# 参数设置
S0 = 772.68         # 初始价格
T = 183 / 252       # 183天约等于0.726年
r = 0.014509        # 无风险利率
sigma = 0.1437      # 年化波动率
n_sim = 20000       # 模拟次数
Z = np.random.randn(n_sim)

# 期末价格模拟公式
ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)

# 绘制直方图
plt.figure(figsize=(10, 5))
plt.hist(ST, bins=50, edgecolor='black')
plt.title("Figure 3-4: Distribution of 20,000 Simulated Final Prices of Gold")
plt.xlabel("Simulated Final Price (RMB/gram)")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()