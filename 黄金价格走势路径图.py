import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 读取真实黄金收盘价并画图：
df = pd.read_excel("/Users/arshwu/Desktop/【合并】每日行情.xlsx")
df = df[df["合约"] == "Au99.99"]
df["日期"] = pd.to_datetime(df["日期"])
df = df.sort_values("日期")
date_range = df["日期"]
S = df["收盘价"]

# 模拟参数
S0 = 772.68            # 起始价格（你期末收盘价）
T = 183 / 252          # 存续期约为 183 天，按 252 交易日计
r = 0.014509           # 无风险利率 1.4509%
sigma = 0.1437         # 年化波动率
N = 125                # 模拟步数（125个交易日）
dt = T / N             # 每一步时间间隔

# 构造一条模拟路径
# np.random.seed(42)
# Z = np.random.normal(0, 1, N)
# drift = (r - 0.5 * sigma**2) * dt
# diffusion = sigma * np.sqrt(dt) * Z
# S = S0 * np.exp(np.cumsum(drift + diffusion))

# date_range = pd.date_range(start="2024-01-01", periods=N, freq="B")  # business days


# 绘图
plt.figure(figsize=(10, 5))
plt.plot(date_range, S)
plt.title('Figure 3-3: Simulated Gold Price Path')
plt.xlabel('Trading Days')
plt.ylabel('Price (RMB/gram)')
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()