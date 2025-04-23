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

st.set_page_config(page_title="S&P 500 Max Drawdown Analysis", layout="wide")
st.title("📉 S&P 500 Max Drawdown Analysis Tool")
start_date = st.date_input("Select start date", value=pd.to_datetime("1955-01-01"))

# Always calculate and display charts and stats on page load
daily_data, annual_data, current_mdd, percentile = calculate_mdd(start_date=start_date)

st.subheader("📊 Daily Maximum Drawdown")
st.line_chart(daily_data['Max Drawdown'])

st.subheader("📆 Annual Maximum Drawdown")
st.bar_chart(data=annual_data.set_index(annual_data['Date'].dt.year)['Max Drawdown'])

st.subheader("🧮 Statistical Summary")
st.write(f"Current Maximum Drawdown: **{current_mdd:.2%}**")
st.write(f"Historical Percentile: **{percentile:.2f}%**")

if percentile <= 10:
    st.warning("📉 The market is in an extreme drawdown (bottom 10%) — possible buying opportunity")
elif percentile <= 30:
    st.info("🔍 The market is in a relatively large drawdown (bottom 30%) — potential opportunity")
else:
    st.success("📈 The market is not in a major drawdown — proceed with caution")
