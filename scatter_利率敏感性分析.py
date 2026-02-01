import matplotlib.pyplot as plt
import pandas as pd

import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 数据准备
data = {
    "无风险利率": [0.01615, 0.01635, 0.01655, 0.01675, 0.01695],
    "债券理论价值": [9919.36, 9918.36, 9917.37, 9916.37, 9915.38],
    "期权理论价值": [147.61, 147.59, 147.58, 147.56, 147.55],
    "产品理论价值": [10066.96, 10065.95, 10064.94, 10063.93, 10062.93]
}
df = pd.DataFrame(data)

# 图3-6：债券价值
plt.figure(figsize=(6, 4))
plt.scatter(df["无风险利率"], df["债券理论价值"], color='blue')
for i in range(len(df)):
    plt.text(df["无风险利率"][i], df["债券理论价值"][i] + 0.2, f'{df["债券理论价值"][i]:.2f}', ha='center')
plt.xlabel("无风险利率（%）")
plt.ylabel("债券理论价值（元）")
plt.xticks(df["无风险利率"], [f"{r*100:.3f}%" for r in df["无风险利率"]])
plt.title("无风险利率与债券理论价值的关系")
plt.grid(True)
plt.tight_layout()
plt.savefig("无风险利率与债券理论价值的关系.png")
plt.show()
plt.close()

# 图3-7：期权价值
plt.figure(figsize=(6, 4))
plt.scatter(df["无风险利率"], df["期权理论价值"], color='blue')
for i in range(len(df)):
    plt.text(df["无风险利率"][i], df["期权理论价值"][i] + 0.05, f'{df["期权理论价值"][i]:.2f}', ha='center')
plt.xlabel("无风险利率（%）")
plt.ylabel("期权理论价值（元）")
plt.xticks(df["无风险利率"], [f"{r*100:.3f}%" for r in df["无风险利率"]])
plt.ylim(147.50, 147.80)
plt.title("无风险利率与期权理论价值的关系")
plt.grid(True)
plt.tight_layout()
plt.savefig("无风险利率与期权理论价值的关系.png")
plt.show()
plt.close()

# 图3-8：产品总价值
plt.figure(figsize=(6, 4))
plt.scatter(df["无风险利率"], df["产品理论价值"], color='blue')
for i in range(len(df)):
    plt.text(df["无风险利率"][i], df["产品理论价值"][i] + 0.5, f'{df["产品理论价值"][i]:.2f}', ha='center')
plt.xlabel("无风险利率（%）")
plt.ylabel("产品理论价值（元）")
plt.xticks(df["无风险利率"], [f"{r*100:.3f}%" for r in df["无风险利率"]])
plt.ylim(10062, 10068)
plt.title("无风险利率与产品理论价值的关系")
plt.grid(True)
plt.tight_layout()
plt.savefig("无风险利率与产品理论价值的关系.png")
plt.show()
plt.close()