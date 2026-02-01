#!/usr/bin/env python3
# akshare_au99.py

import akshare as ak
import pandas as pd

def main():
    # 1. 获取所有 Au99.99 日度历史数据
    df = ak.spot_hist_sge(symbol="Au99.99")

    # 2. 筛选并重命名列
    # 注意：如果 akshare 版本里列名不一样，请先 print(df.columns) 看下再对应修改
    df = df[[
        "date",           # 交易日期
        "open",           # 开盘价
        "high",           # 最高价
        "low",            # 最低价
        "close",          # 收盘价
        "change",         # 涨跌
        "change_rate",    # 涨跌幅 (%)
        "average_price",  # 加权平均价
        "volume",         # 成交量
        "turnover"        # 成交金额
    ]]
    df.columns = [
        "日期",
        "开盘价",
        "最高价",
        "最低价",
        "收盘价",
        "涨跌",
        "涨跌幅",
        "加权平均价",
        "成交量",
        "成交金额"
    ]

    # 3. 筛选时间区间
    df["日期"] = pd.to_datetime(df["日期"])
    df = df[(df["日期"] >= "2022-06-01") & (df["日期"] <= "2025-06-01")]

    # 4. 导出 CSV（UTF-8 带 BOM）
    out_file = "Au99.99_2022-06_to_2025-06.csv"
    df.to_csv(out_file, index=False, encoding="utf-8-sig")
    print(f"✅ 已保存：{out_file}")

if __name__ == "__main__":
    main()