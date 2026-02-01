import pandas as pd
import os

# Print current directory to help locate the Excel file
print("Files in current directory:", os.listdir('.'))
#
# 自动检测包含“合并”或“行情”关键字的 Excel 文件
files = [f for f in os.listdir('.') if f.lower().endswith(('.xlsx', '.xls'))]
candidates = [f for f in files if '合并' in f or '行情' in f]
if len(candidates) == 1:
    excel_file = candidates[0]
    print(f"Auto-detected Excel file: '{excel_file}'")
elif len(candidates) > 1:
    print("Multiple candidate files found:", candidates)
    excel_file = candidates[0]
    print(f"Defaulting to first: '{excel_file}'")
else:
    # 尝试在用户桌面目录中查找
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.isdir(desktop_dir):
        desktop_files = [f for f in os.listdir(desktop_dir) if f.lower().endswith(('.xlsx', '.xls'))]
        desktop_candidates = [f for f in desktop_files if '合并' in f or '行情' in f]
        if desktop_candidates:
            excel_file = os.path.join(desktop_dir, desktop_candidates[0])
            print(f"Auto-detected Excel file on Desktop: '{excel_file}'")
        else:
            raise FileNotFoundError("在当前目录和桌面均未找到包含“合并”或“行情”关键字的 Excel 文件，请检查目录。")
    else:
        raise FileNotFoundError("桌面目录不存在，且在当前目录未找到目标 Excel 文件。")

# 1. 读取数据
df = pd.read_excel(excel_file)
# 标准化列名：去除前后空白和 BOM
df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=False)
print("Data columns:", df.columns.tolist())
# 确保有'日期'列，如果没有则将第一列重命名为'日期'
if '日期' not in df.columns:
    original_date_col = df.columns[0]
    print(f"Renaming column '{original_date_col}' to '日期'")
    df.rename(columns={original_date_col: '日期'}, inplace=True)
# 转换日期类型
df['日期'] = pd.to_datetime(df['日期'])

# 确保有'收盘价'列，如果没有则尝试根据列名关键字重命名
if '收盘价' not in df.columns:
    # 寻找包含“收盘”字样的列
    candidates = [col for col in df.columns if '收盘' in col]
    if candidates:
        original_price_col = candidates[0]
        df.rename(columns={original_price_col: '收盘价'}, inplace=True)
        print(f"Renamed column '{original_price_col}' to '收盘价'")
    else:
        raise KeyError("未找到包含“收盘”字样的列，请检查表格列名")

# 2. 确定期初价格 S0 和观察期
start_date = pd.Timestamp('2025-06-10')
df = df.sort_values('日期')
S0 = df.loc[df['日期'] == start_date, '收盘价'].iloc[0]

# 3. 定义双层区间阈值
inner_low, inner_up = S0 * 0.98, S0 * 1.06
outer_low, outer_up = S0 * 0.97, S0 * 1.10

# 4. 统计各区间天数
def classify(price):
    if inner_low <= price <= inner_up:
        return 'D1'
    elif outer_low <= price < inner_low or inner_up < price <= outer_up:
        return 'D2'
    else:
        return 'D3'

df['区间'] = df['收盘价'].apply(classify)
counts = df['区间'].value_counts()
D1 = counts.get('D1', 0)
D2 = counts.get('D2', 0)
D3 = counts.get('D3', 0)
N = D1 + D2 + D3

# 5. 参数设置
r_base = 0.01655   # 1.655%
y1 = 0.078         # 内层区间浮动 7.8%
y2 = 0.045         # 外层区间内浮动 4.5%
y3 = 0.025         # 外层区间外浮动 2.5%

# 6. 计算预期年化收益率
R = r_base + (D1/N)*y1 + (D2/N)*y2 + (D3/N)*y3

# 7. 输出结果
print(f"初始价格 S0 = {S0:.2f} 元/克")
print(f"观察总天数 N = {N} 天 (D1={D1}, D2={D2}, D3={D3})")
print(f"预期年化收益率 R = {R*100:.2f}%")