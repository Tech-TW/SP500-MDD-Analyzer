import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 計算最大跌幅資料
def calculate_mdd(start_date="1955-01-01"):
    sp500 = yf.download("^GSPC", start=start_date, progress=False)
    sp500 = sp500['Close']
    sp500 = sp500.resample('D').ffill()
    drawdown = (sp500 - sp500.cummax()) / sp500.cummax()
    drawdown.name = "Max Drawdown"
    daily_data = pd.DataFrame({"Date": sp500.index, "Max Drawdown": drawdown.values.flatten()})
    daily_data.set_index("Date", inplace=True)
    annual_data = daily_data.resample('YE').agg({'Max Drawdown': 'min'}).reset_index()
    current_mdd = daily_data['Max Drawdown'].iloc[-1]
    percentile = (daily_data['Max Drawdown'] < current_mdd).mean() * 100
    return daily_data, annual_data, current_mdd, percentile

# Streamlit 介面設置
st.set_page_config(page_title="S&P 500 Max Drawdown Analysis", layout="wide")
st.title("📉 S&P 500 Max Drawdown Analysis Tool")

start_date = st.date_input("Select start date", value=pd.to_datetime("1955-01-01"))
daily_data, annual_data, current_mdd, percentile = calculate_mdd(start_date=start_date)

# 折線圖：每日最大跌幅 + 水平線
st.subheader("📊 Daily Maximum Drawdown")
fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(daily_data.index, daily_data['Max Drawdown'], label='Daily Max Drawdown')
ax1.axhline(y=current_mdd, color='red', linestyle='--', label=f'Current MDD: {current_mdd:.2%}')
ax1.set_title("Daily Max Drawdown with Current MDD Line")
ax1.set_ylabel("Drawdown")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# 長條圖：年度最大跌幅 + 水平線
st.subheader("📆 Annual Maximum Drawdown")
fig2, ax2 = plt.subplots(figsize=(12, 4))
years = annual_data['Date'].dt.year
ax2.bar(years, annual_data['Max Drawdown'], label='Annual Max Drawdown')
ax2.axhline(y=current_mdd, color='red', linestyle='--', label=f'Current MDD: {current_mdd:.2%}')
ax2.set_title("Annual Max Drawdown with Current MDD Line")
ax2.set_ylabel("Drawdown")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# 統計數據與說明
st.subheader("🧮 Statistical Summary")
st.write(f"Current Maximum Drawdown: **{current_mdd:.2%}**")
st.write(f"Historical Percentile: **{percentile:.2f}%**")

# 風險訊號提示
if percentile <= 10:
    st.warning("📉 The market is in an extreme drawdown (bottom 10%) — possible buying opportunity")
elif percentile <= 30:
    st.info("🔍 The market is in a relatively large drawdown (bottom 30%) — potential opportunity")
else:
    st.success("📈 The market is not in a major drawdown — proceed with caution")
