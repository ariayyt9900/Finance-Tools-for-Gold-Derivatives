import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties

# 设置中文字体支持和负号正常显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 若无 SimHei，可改为系统中其他中文字体名
plt.rcParams['axes.unicode_minus'] = False

# 指定中文字体文件路径（macOS示例）
font_ch = FontProperties(fname='/System/Library/Fonts/STHeiti Light.ttc')

# 参数设置
r_base = 0.01655  # 基础保底收益率
y1 = 0.078        # 内层区间收益率
y2 = 0.045        # 外层区间内段收益率
y3 = 0.025        # 外层区间外段收益率

# 构造 D1/N 与 D2/N 网格
grid_size = 50
d1 = np.linspace(0, 1, grid_size)
d2 = np.linspace(0, 1, grid_size)
D1, D2 = np.meshgrid(d1, d2)

# 计算年化收益率 R
R = r_base + y1 * D1 + y2 * D2 + y3 * (1 - D1 - D2)

# 绘制 3D 曲面图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(D1, D2, R, cmap='winter')

# 设置轴标签和标题
ax.set_xlabel('内层区间天数比例 D1/N', fontproperties=font_ch)
ax.set_ylabel('外层内段天数比例 D2/N', fontproperties=font_ch)
ax.set_zlabel('年化收益率 R', fontproperties=font_ch)
ax.set_title('爱康无忧产品年化收益率结构图', fontproperties=font_ch)

plt.tight_layout()
plt.show()