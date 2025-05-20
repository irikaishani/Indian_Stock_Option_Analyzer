import streamlit as st
import requests
import streamlit.components.v1 as components
import urllib.parse

st.set_page_config(page_title="Home - Option Analyzer", layout="wide", page_icon="📈")

# --- LOTTIE EMBED VIA HTML ---
def show_lottie_html(url: str, height: int = 300):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            st.warning("⚠️ Could not load animation.")
            return
        animation_json = r.text
        html = f"""
        <div id="lottie" style="width:100%; height:{height}px;"></div>
        <script src="https://unpkg.com/lottie-web@latest/build/player/lottie.min.js"></script>
        <script>
          var animationData = {animation_json};
          lottie.loadAnimation({{
            container: document.getElementById('lottie'),
            renderer: 'svg',
            loop: true,
            autoplay: true,
            animationData: animationData
          }});
        </script>
        """
        components.html(html, height=height + 50)
    except Exception as e:
        st.error(f"Error loading animation: {e}")

# --- PAGE HEADER ---
st.markdown("<h1 style='text-align:center; color:#4CAF50;'>📈 Indian Stock Option Analyzer</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- TWO-COLUMN INTRO & ANIMATION ---
col1, col2 = st.columns([1.4, 1])
with col1:
    st.markdown("### 🚀 How to Use")
    st.markdown("""
Welcome to the **Indian Stock Option Analyzer**, your 2-step assistant for real-time option analysis and AI-powered trading insights.

**Steps:**
1. 👉 Go to **Select Option** in the sidebar.
2. 📊 Then move to **Analyze Option** to fetch live Upstox data.
3. 🤖 Click **“Get AI Suggestion”** for smart trading recommendations.
    """)
    st.markdown("⬅️ Use the sidebar to navigate.")
    st.markdown("📅 Built for traders in 2025 and beyond.")
with col2:
    show_lottie_html("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json", height=300)

# --- FEATURES SECTION ---
st.markdown("---")
st.markdown("### 🔍 Features")
st.markdown("""
- ✅ Real-time NSE Option Chain Data  
- 💰 Live Premium & Market Price  
- 📈 Option Greeks (Delta, Gamma, Theta, Vega, IV)  
- 🤖 AI-Powered Buy/Sell/Hold Suggestions via **Groq LLM**  
- 🧠 Smart strategy hints: spreads, straddles, hedges  
""")

# --- QUICK NAVIGATION BUTTONS ---
st.markdown("---")
st.markdown("### 🚀 Quick Navigation")
colA, colB = st.columns(2)
with colA:
    if st.button("➡️ Select Option"):
        st.switch_page("pages/1_Phase_1_Select_Option.py")
with colB:
    if st.button("➡️ Analyze Option"):
        st.switch_page("pages/2_Phase_2_Analyze_Option.py")


# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>Built with ❤️ by <strong>Irika Ishani</strong> using <strong>Upstox</strong> + <strong>Groq AI</strong> • 2025 Option Analyzer</p>",
    unsafe_allow_html=True,
)
