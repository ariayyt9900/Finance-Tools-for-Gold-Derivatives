import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 模拟参数
S0 = 772.68             # 初始价格（2025.6.10收盘价）
T = 183 / 252           # 存续期折算为年
r = 0.014509            # 无风险利率（年化）
sigma = 0.1437          # 年化波动率
n_sim = 20000           # 模拟次数

# 生成标准正态分布随机变量
Z = np.random.randn(n_sim)

# 模拟黄金期末价格路径
ST = S0 * np.exp((r - 0.5 * sigma ** 2) * T + sigma * np.sqrt(T) * Z)

# 定义结构性理财产品收益函数
def calculate_return(price):
    if price < 800:
        return 0.00
    elif price < 1000:
        return 0.03
    else:
        return 0.08

# 计算每条模拟路径对应的产品收益
returns = np.array([calculate_return(p) for p in ST])

# 统计收益分布
return_bins = [0.00, 0.03, 0.08, np.inf]
return_labels = ["0%", "3%", "8%+"]
return_categories = pd.cut(returns, bins=return_bins, labels=return_labels, right=False)
return_table = return_categories.value_counts().sort_index().to_frame(name="次数")
return_table["概率"] = (return_table["次数"] / n_sim * 100).round(2)

# 输出收益分布表
print("结构性理财产品收益分布（表3-2）：")
print(return_table)

# 重新定义价格区间
bins = [0, 800, 1000, np.inf]
labels = ["(0, 800)", "[800, 1000)", "[1000, +∞)"]

# 分类统计
categories = pd.cut(ST, bins=bins, labels=labels)
table = categories.value_counts().sort_index().to_frame(name="次数")
table["概率"] = (table["次数"] / n_sim * 100).round(2)

# 输出表格数据
print("模拟结果分布（表3-1）：")
print(table)

# ---------------- 可视化黄金价格分布 ----------------
# 可视化直方图
plt.figure(figsize=(10, 5))
plt.hist(ST, bins=50, edgecolor='black')
plt.title("Figure 3-4: Distribution of 20,000 Simulated Final Prices of Gold")
plt.xlabel("Simulated Final Price (RMB/gram)")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()