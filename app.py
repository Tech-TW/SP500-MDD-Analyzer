import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

st.set_page_config(page_title="S&P 500 最大跌幅分析", layout="wide")
st.title("📉 S&P 500 最大跌幅分析工具")
start_date = st.date_input("選擇起始日期", value=pd.to_datetime("1955-01-01"))

if st.button("開始分析"):
    with st.spinner("抓取資料與分析中..."):
        daily_data, annual_data, current_mdd, percentile = calculate_mdd(start_date=start_date)
    st.success("分析完成！")

    st.subheader("📊 每日最大跌幅")
    st.line_chart(daily_data['Max Drawdown'])

    st.subheader("📆 年度最大跌幅")
    st.bar_chart(data=annual_data.set_index(annual_data['Date'].dt.year)['Max Drawdown'])

    st.subheader("🧮 統計結果")
    st.write(f"目前最大跌幅：**{current_mdd:.2%}**")
    st.write(f"歷史分位數：**{percentile:.2f}%**")
    if percentile <= 10:
        st.warning("📉 現在處於歷史極端跌幅（前10%）——進場機會可能較佳")
    elif percentile <= 30:
        st.info("🔍 現在處於相對較大跌幅區間（前30%）——可觀察潛在機會")
    else:
        st.success("📈 現在市場尚未進入明顯下跌區間——進場需更謹慎")
