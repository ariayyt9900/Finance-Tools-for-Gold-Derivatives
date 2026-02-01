import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # macOS中文支持
matplotlib.rcParams['axes.unicode_minus'] = False

# 假设你已读取并整理好“每日行情数据”的DataFrame为 df，列名包括“加权平均价”
# 读取 Excel 文件
df = pd.read_excel("/Users/arshwu/Desktop/【合并】每日行情.xlsx", sheet_name="每日行情数据")
# 并按时间升序排列
df = df.sort_values(by="日期")
prices = df["加权平均价"].values

# 计算对数收益率
log_returns = np.diff(np.log(prices))

# 参数估计
mu = np.mean(log_returns)
sigma = np.std(log_returns)
S0 = prices[-1]  # 当前黄金价格
T = 1  # 模拟1年
n_simulations = 20000

# 蒙特卡洛模拟未来价格
np.random.seed(0)
Z = np.random.randn(n_simulations)
ST = S0 * np.exp((mu - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

# 自定义年化收益率区间（与收益结构挂钩）
bins = [0.02, 0.022, 0.024, 0.026, 0.028, 0.03, 0.032, 0.034, 0.036, 0.038, 0.04]
labels = [f"{b:.3f}" for b in bins]

# Bull spread 收益结构模拟
lower_bound = S0 * 0.975   # 恢复稍宽上下限
upper_bound = S0 * 1.025

mapped_returns = []
for price in ST:
    if price <= lower_bound:
        mapped_returns.append(0.02)
    elif price >= upper_bound:
        mapped_returns.append(0.04)
    else:
        r = 0.02 + (price - lower_bound) / (upper_bound - lower_bound) * 0.02
        if r < 0.023:
            mapped_returns.append(0.022)
        elif r < 0.025:
            mapped_returns.append(0.024)
        elif r < 0.027:
            mapped_returns.append(0.026)
        elif r < 0.029:
            mapped_returns.append(0.028)
        elif r < 0.031:
            mapped_returns.append(0.03)
        elif r < 0.033:
            mapped_returns.append(0.032)
        elif r < 0.035:
            mapped_returns.append(0.034)
        elif r < 0.037:
            mapped_returns.append(0.036)
        elif r < 0.039:
            mapped_returns.append(0.038)
        else:
            mapped_returns.append(0.04)

# 将收益率四舍五入统一为固定档位
mapped_returns = [round(r, 3) for r in mapped_returns]

# 获取唯一的档位并排序
unique_bins = sorted(set(mapped_returns))

# 统计每个档位的频数
counts = [mapped_returns.count(b) for b in bins]

# 标签更新
labels = [str(b) for b in bins]

# 构建频数表
result_df = pd.DataFrame({
    "预期年化收益率": labels,
    "频数": counts
})

# 输出结果
print(result_df)

# 可视化
plt.figure(figsize=(10, 5))
plt.bar(labels, counts, color='skyblue')
plt.xlabel("预期年化收益率（单位：%）")
plt.ylabel("频数（单位：次）")
plt.title("图3-5 '爱康无忧'产品年化收益率模拟分布")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# 为每根柱子标注频数
for i, count in enumerate(counts):
    plt.text(i, count + 100, str(count), ha='center', va='bottom', fontsize=9)

# 保存图表为图片
plt.savefig("爱康无忧_年化收益率分布图.png")
plt.show()