import streamlit as st
import requests
from datetime import datetime
import json
from dotenv import load_dotenv
import upstox_client
from groq import Groq
import gzip
import io
import os
import pandas as pd

st.set_page_config(page_title="Phase 2 - Option Data", layout="wide", page_icon="📊")
st.title("📊 Phase 2: Analyze Option Data")
st.markdown("---")

# 🔐 Validate session
if "selection" not in st.session_state:
    st.warning("⚠️ Please go to Phase 1 and select an option.")
    st.stop()

# 🔐 Load API keys
load_dotenv()
access_token = os.getenv("UPSTOX_ACCESS_TOKEN")
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

# 🧠 Upstox Setup
configuration = upstox_client.Configuration()
configuration.access_token = access_token
api_client = upstox_client.ApiClient(configuration)

# 🎯 Extract selected data
sel = st.session_state["selection"]
symbol, expiry, strike, option_type = sel["symbol"], sel["expiry"], sel["strike"], sel["option_type"]
expiry_iso = datetime.strptime(expiry, "%d%b%Y").strftime("%Y-%m-%d")
st.caption(f"📆 Expiry Date (ISO): `{expiry_iso}`")

# 📦 Fetch instrument_key and asset_key
@st.cache_data
def fetch_contract_keys():
    url = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"
    res = requests.get(url)
    with gzip.GzipFile(fileobj=io.BytesIO(res.content)) as f:
        data = json.load(f)
    for item in data:
        try:
            if item.get("name") == symbol and \
               datetime.utcfromtimestamp(item["expiry"]/1000).strftime("%d%b%Y").upper() == expiry and \
               item.get("strike_price") == strike and \
               item.get("instrument_type") == option_type:
                return item.get("instrument_key"), item.get("asset_key")
        except:
            continue
    return None, None

instrument_key, asset_key = fetch_contract_keys()

if not instrument_key or not asset_key:
    st.error("❌ Could not find matching instrument.")
    st.stop()

# 🔍 Fetch Option Chain
url = 'https://api.upstox.com/v2/option/chain'
headers = {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
params = {"instrument_key": asset_key, "expiry_date": expiry_iso}
res = requests.get(url, params=params, headers=headers).json()
chain_data = res.get("data", [])

def match_token(item):
    key = "call_options" if option_type == "CE" else "put_options"
    return item.get("strike_price") == strike and item.get(key, {}).get("instrument_key") == instrument_key

matched = next((item for item in chain_data if match_token(item)), None)

if not matched:
    st.error("❌ No matching contract in option chain.")
    st.stop()

opt_data = matched["call_options"] if option_type == "CE" else matched["put_options"]

# 📋 Display Contract Summary
col1, col2 = st.columns(2)
summary = {
    "Underlying": symbol,
    "Expiry": expiry,
    "Strike": strike,
    "Type": option_type
}

with col1:
    st.subheader("📋 Contract Summary")
    st.markdown(f"""
    - **Underlying**: `{symbol}`  
    - **Expiry**: `{expiry}`  
    - **Strike Price**: `₹{strike}`  
    - **Option Type**: `{option_type}`
    """)

with col2:
    st.subheader("💰 Live Market Price")
    ltp = opt_data.get("market_data", {}).get("ltp")
    st.metric("Premium (₹)", f"{ltp:.2f}" if ltp else "N/A")

# 📊 Market Data Table
with st.expander("📊 Market Data"):
    market_data = opt_data.get("market_data", {})
    if market_data:
        st.markdown("#### 📈 Live Market Metrics")
        market_df = pd.DataFrame(market_data.items(), columns=["Metric", "Value"])
        st.dataframe(market_df, use_container_width=True)
    else:
        st.info("No market data available.")

# 📈 Option Greeks Table
with st.expander("📈 Option Greeks"):
    greeks = opt_data.get("option_greeks", {})
    if greeks:
        st.markdown("#### 🧮 Calculated Greeks")
        greeks_df = pd.DataFrame(greeks.items(), columns=["Greek", "Value"])
        st.dataframe(greeks_df, use_container_width=True)
    else:
        st.info("No Greeks available for this contract.")

# 🔄 Save to session for Groq
st.session_state["opt_data"] = opt_data
st.session_state["contract_summary"] = summary

# 🤖 Groq AI Analysis
if st.button("🤖 Get AI Suggestion with Groq"):
    prompt = f"""
You are a senior options trading strategist at a hedge fund with deep experience in analyzing Indian stock options using market data and Greeks.

You are given the data of a selected option contract. Based on this, provide a detailed professional trading recommendation using the following format:

---
**RECOMMENDATION**: [BUY / SELL / HOLD]  
**CONFIDENCE (0-100%)**: [e.g. 85%]  

**REASONING**: Provide 10–20 short bullet points based on:
- Premium level
- Implied volatility
- Option Greeks (especially Delta, Theta, Vega, Gamma)
- Moneyness (ITM/ATM/OTM)
- Time decay
- Liquidity or spread
- Underlying strength or weakness
- Broader market conditions (if inferable)
- Support/resistance relative to strike
- Any skew/volatility clues
- Probabilities of profit or risk
- Volume or OI (if available)

**SUGGESTED STRATEGY**:
Recommend an appropriate strategy such as:
- Long/Short Call or Put
- Bull Call Spread, Bear Put Spread
- Iron Condor, Straddle, Strangle
- Calendar spread or ratio spread

Explain:
- Entry logic
- Max gain/loss
- Breakeven levels
- Ideal market movement or expiry outcome
- Risk level (Low/Moderate/High)

---
Be concise but professional. Avoid unnecessary disclaimers. Write in markdown.

### Contract Summary:
{json.dumps(summary, indent=2)}

### Market Data:
{json.dumps(opt_data.get("market_data", {}), indent=2)}

### Option Greeks:
{json.dumps(opt_data.get("option_greeks", {}), indent=2)}
"""
    with st.spinner("💡 Analyzing with Groq..."):
        try:
            response = groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            result = response.choices[0].message.content
            st.success("✅ AI Suggestion Ready")
            st.markdown("### 🧠 AI Trading Recommendation")
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ Groq API error: {e}")

# # 🔁 Analyze another stock
# st.markdown("---")
# if st.button("🔁 Analyze Another Stock"):
#     for key in ["selection", "opt_data", "contract_summary"]:
#         if key in st.session_state:
#             del st.session_state[key]
#     st.success("🔄 Session cleared. Redirecting to Select Option...")
#     st.switch_page("pages/1_Phase_1_Select_Option.py")
