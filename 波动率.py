import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

# 设置中文字体（适用于 macOS）
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['PingFang SC', 'SimHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 数据准备
data = {
    "波动率": [0.04, 0.09, 0.14, 0.19, 0.24],
    "期权理论价值": [126.73, 122.20, 120.31, 118.78, 118.32],
    "产品理论价值": [10044.10, 10039.57, 10037.67, 10036.14, 10035.69]
}
df = pd.DataFrame(data)

# 图1：波动率与期权理论价值的关系
plt.figure(figsize=(6, 4))
plt.scatter(df["波动率"], df["期权理论价值"], color='blue')
for i in range(len(df)):
    plt.text(df["波动率"][i], df["期权理论价值"][i] + 0.1, f'{df["期权理论价值"][i]:.2f}', ha='center')
plt.xlabel("波动率")
plt.ylabel("期权理论价值（元）")
plt.title("波动率与期权理论价值的关系")
plt.grid(True)
plt.tight_layout()
plt.savefig("波动率与期权理论价值的关系.png")
plt.show()

# 图2：波动率与产品理论价值的关系
plt.figure(figsize=(6, 4))
plt.scatter(df["波动率"], df["产品理论价值"], color='blue')
for i in range(len(df)):
    plt.text(df["波动率"][i], df["产品理论价值"][i] + 0.5, f'{df["产品理论价值"][i]:.2f}', ha='center')
plt.xlabel("波动率")
plt.ylabel("产品理论价值（元）")
plt.title("波动率与产品理论价值的关系")
plt.grid(True)
plt.tight_layout()
plt.savefig("波动率与产品理论价值的关系.png")
plt.show()