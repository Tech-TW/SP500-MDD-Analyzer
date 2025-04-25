import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

# 計算最大跌幅
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

# 初始化頁面
st.set_page_config(page_title="Max Drawdown Analysis", layout="wide")
st.title("📉 Global Index Max Drawdown Analysis Tool")

# ========= S&P 500 =========
st.header("🇺🇸 S&P 500")
start_date_spx = st.date_input("Select start date for S&P 500", value=pd.to_datetime("1955-01-01"), key="spx_date")
daily_spx, annual_spx, mdd_spx, pct_spx = calculate_mdd("^GSPC", start_date=start_date_spx)

# 每日 MDD 折線圖 + 當前水平線與標籤
daily_chart_spx = alt.Chart(daily_spx.reset_index()).mark_line().encode(
    x='Date:T',
    y=alt.Y('Max Drawdown:Q', scale=alt.Scale(domain=[-1, 0]))
)

rule_spx = alt.Chart(pd.DataFrame({'y': [mdd_spx]})).mark_rule(color='red', strokeDash=[4, 4]).encode(y='y:Q')

label_spx = alt.Chart(daily_spx.reset_index()).transform_filter(
    alt.datum.Date == daily_spx.index[-1].strftime("%Y-%m-%d")
).mark_text(
    align='left', dx=5, dy=-10, color='red'
).encode(
    x='Date:T',
    y='Max Drawdown:Q',
    text=alt.value(f"Current: {mdd_spx:.2%}")
)

st.subheader("📊 Daily Maximum Drawdown - S&P 500")
st.altair_chart(daily_chart_spx + rule_spx + label_spx, use_container_width=True)

# 年度 MDD 長條圖 + 當前水平線
annual_chart_spx = alt.Chart(annual_spx).mark_bar().encode(
    x=alt.X('year(Date):O', title="Year"),
    y=alt.Y('Max Drawdown:Q', scale=alt.Scale(domain=[-1, 0]))
)

rule_annual_spx = alt.Chart(pd.DataFrame({'y': [mdd_spx]})).mark_rule(color='red', strokeDash=[4, 4]).encode(y='y:Q')

st.subheader("📆 Annual Maximum Drawdown - S&P 500")
st.altair_chart(annual_chart_spx + rule_annual_spx, use_container_width=True)

st.subheader("🧮 Statistical Summary - S&P 500")
st.write(f"Current Maximum Drawdown: **{mdd_spx:.2%}**")
st.write(f"Historical Percentile: **{pct_spx:.2f}%**")
if pct_spx <= 10:
    st.warning("📉 The S&P 500 is in an extreme drawdown (bottom 10%) — possible buying opportunity")
elif pct_spx <= 30:
    st.info("🔍 The S&P 500 is in a relatively large drawdown (bottom 30%) — potential opportunity")
else:
    st.success("📈 The S&P 500 is not in a major drawdown — proceed with caution")

# ========= TWII =========
st.header("🇹🇼 Taiwan Weighted Index")
start_date_twii = st.date_input("Select start date for Taiwan Weighted Index", value=pd.to_datetime("1990-01-01"), key="twii_date")
daily_twii, annual_twii, mdd_twii, pct_twii = calculate_mdd("^TWII", start_date=start_date_twii)

# 每日 MDD 折線圖 + 當前水平線與標籤
daily_chart_twii = alt.Chart(daily_twii.reset_index()).mark_line().encode(
    x='Date:T',
    y=alt.Y('Max Drawdown:Q', scale=alt.Scale(domain=[-1, 0]))
)

rule_twii = alt.Chart(pd.DataFrame({'y': [mdd_twii]})).mark_rule(color='red', strokeDash=[4, 4]).encode(y='y:Q')

label_twii = alt.Chart(daily_twii.reset_index()).transform_filter(
    alt.datum.Date == daily_twii.index[-1].strftime("%Y-%m-%d")
).mark_text(
    align='left', dx=5, dy=-10, color='red'
).encode(
    x='Date:T',
    y='Max Drawdown:Q',
    text=alt.value(f"Current: {mdd_twii:.2%}")
)

st.subheader("📊 Daily Maximum Drawdown - TWII")
st.altair_chart(daily_chart_twii + rule_twii + label_twii, use_container_width=True)

# 年度 MDD 長條圖 + 當前水平線
annual_chart_twii = alt.Chart(annual_twii).mark_bar().encode(
    x=alt.X('year(Date):O', title="Year"),
    y=alt.Y('Max Drawdown:Q', scale=alt.Scale(domain=[-1, 0]))
)

rule_annual_twii = alt.Chart(pd.DataFrame({'y': [mdd_twii]})).mark_rule(color='red', strokeDash=[4, 4]).encode(y='y:Q')

st.subheader("📆 Annual Maximum Drawdown - TWII")
st.altair_chart(annual_chart_twii + rule_annual_twii, use_container_width=True)

st.subheader("🧮 Statistical Summary - TWII")
st.write(f"Current Maximum Drawdown: **{mdd_twii:.2%}**")
st.write(f"Historical Percentile: **{pct_twii:.2f}%**")
if pct_twii <= 10:
    st.warning("📉 The Taiwan Weighted Index is in an extreme drawdown (bottom 10%) — possible buying opportunity")
elif pct_twii <= 30:
    st.info("🔍 The Taiwan Weighted Index is in a relatively large drawdown (bottom 30%) — potential opportunity")
else:
    st.success("📈 The Taiwan Weighted Index is not in a major drawdown — proceed with caution")
