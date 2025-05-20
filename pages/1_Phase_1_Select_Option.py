import streamlit as st
import pandas as pd
import requests
import os
import gzip
import io
import json
from dotenv import load_dotenv
from datetime import datetime
import upstox_client

st.set_page_config(page_title="Phase 1 - Select Option", layout="wide", page_icon="📌")
st.title("📌 Phase 1: Select Option Details")
st.markdown("---")

# 🔐 Load API Keys
load_dotenv()
access_token = os.getenv("UPSTOX_ACCESS_TOKEN")

# 🧠 Initialize Upstox Client
configuration = upstox_client.Configuration()
configuration.access_token = access_token
api_client = upstox_client.ApiClient(configuration)

# 📦 Load NSE Option Master
@st.cache_data(show_spinner="📦 Fetching NSE Option Master...")
def load_option_master():
    url = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"
    response = requests.get(url)
    with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df = df[df['instrument_type'].isin(['OPTSTK', 'OPTIDX', 'EQ', 'CE', 'PE'])]
    df = df[df['exchange'] == 'NSE']
    df['expiry'] = pd.to_datetime(df['expiry'] / 1000, unit='s').dt.strftime('%d%b%Y').str.upper()
    df['strike_price'] = df.get('strike_price', df.get('strike'))
    df.rename(columns={'trading_symbol': 'symbol', 'name': 'name', 'instrument_type': 'type'}, inplace=True)
    return df[['instrument_key', 'symbol', 'name', 'expiry', 'strike_price', 'type', 'asset_key']].dropna()

df = load_option_master()

# 🔹 Option Selection UI
col1, col2, col3 = st.columns(3)
with col1:
    selected_symbol = st.selectbox("📌 Select Underlying", sorted(df['name'].unique()))

filtered = df[df['name'] == selected_symbol]

with col2:
    selected_expiry = st.selectbox("📅 Select Expiry", sorted(filtered['expiry'].unique(), key=lambda x: datetime.strptime(x, "%d%b%Y")))

strike_df = filtered[filtered['expiry'] == selected_expiry]

with col3:
    selected_strike = st.selectbox("💥 Select Strike Price", sorted(strike_df['strike_price'].unique()))

option_type = st.radio("📂 Option Type", ["CE", "PE"], horizontal=True)

# ✅ Confirm and redirect
if st.button("✅ Confirm Selection and Go to Phase 2"):
    st.session_state["selection"] = {
        "symbol": selected_symbol,
        "expiry": selected_expiry,
        "strike": selected_strike,
        "option_type": option_type
    }
    st.success("✅ Selection saved! Redirecting to Phase 2...")

    # Redirect to Phase 2 using streamlit's navigation
    st.switch_page("pages/2_Phase_2_Analyze_Option.py")
