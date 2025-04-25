import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

def calculate_mdd(ticker="^GSPC", start_date="1955-01-01"):
    data = yf.download(ticker, start=start_date, progress=False)
    data = data['Close'].resample('D').ffill()
    drawdown = (data - data.cummax()) / data.cummax()
    drawdown.name = "Max Drawdown"
    daily_data = pd.DataFrame({"Date": data.index, "Max Drawdown": drawdown.values.flatten()})
    daily_data.set_index("Date", inplace=True)
    annual_data = daily_data.resample('YE').agg({'Max Drawdown': 'min'}).reset_index()
    current_mdd = daily_data['Max Drawdown'].iloc[-1]
    percentile = (daily_data['Max Drawdown'] < current_mdd).mean() * 100
    return daily_data, annual_data, current_mdd, percentile

st.set_page_config(page_title="Max Drawdown Analysis", layout="wide")
st.title("📉 Global Index Max Drawdown Analysis Tool")

# ==== S&P 500 區塊 ====
st.header("🇺🇸 S&P 500")
start_date_spx = st.date_input("Select start date for S&P 500", value=pd.to_datetime("1955-01-01"), key="spx_date")
daily_data_spx, annual_data_spx, current_mdd_spx, percentile_spx = calculate_mdd("^GSPC", start_date=start_date_spx)

st.subheader("📊 Daily Maximum Drawdown - S&P 500")
st.line_chart(daily_data_spx['Max Drawdown'])

st.subheader("📆 Annual Maximum Drawdown - S&P 500")
st.bar_chart(data=annual_data_spx.set_index(annual_data_spx['Date'].dt.year)['Max Drawdown'])

st.subheader("🧮 Statistical Summary - S&P 500")
st.write(f"Current Maximum Drawdown: **{current_mdd_spx:.2%}**")
st.write(f"Historical Percentile: **{percentile_spx:.2f}%**")

if percentile_spx <= 10:
    st.warning("📉 The S&P 500 is in an extreme drawdown (bottom 10%) — possible buying opportunity")
elif percentile_spx <= 30:
    st.info("🔍 The S&P 500 is in a relatively large drawdown (bottom 30%) — potential opportunity")
else:
    st.success("📈 The S&P 500 is not in a major drawdown — proceed with caution")

# ==== 台灣加權指數 區塊 ====
st.header("🇹🇼 Taiwan Weighted Index")
start_date_twii = st.date_input("Select start date for Taiwan Weighted Index", value=pd.to_datetime("1990-01-01"), key="twii_date")
daily_data_twii, annual_data_twii, current_mdd_twii, percentile_twii = calculate_mdd("^TWII", start_date=start_date_twii)

st.subheader("📊 Daily Maximum Drawdown - TWII")
st.line_chart(daily_data_twii['Max Drawdown'])

st.subheader("📆 Annual Maximum Drawdown - TWII")
st.bar_chart(data=annual_data_twii.set_index(annual_data_twii['Date'].dt.year)['Max Drawdown'])

st.subheader("🧮 Statistical Summary - TWII")
st.write(f"Current Maximum Drawdown: **{current_mdd_twii:.2%}**")
st.write(f"Historical Percentile: **{percentile_twii:.2f}%**")

if percentile_twii <= 10:
    st.warning("📉 The Taiwan Weighted Index is in an extreme drawdown (bottom 10%) — possible buying opportunity")
elif percentile_twii <= 30:
    st.info("🔍 The Taiwan Weighted Index is in a relatively large drawdown (bottom 30%) — potential opportunity")
else:
    st.success("📈 The Taiwan Weighted Index is not in a major drawdown — proceed with caution")
