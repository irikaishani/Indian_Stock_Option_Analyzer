# Indian Stock Option Analyzer

Indian Stock Option Analyzer is a Streamlit-based web application designed to streamline the analysis of stock options using real-time data from the Upstox API and intelligent insights from the Groq API. The app provides option greeks, strike prices, open interest, and recommends actionable strategies like buying/selling based on data-driven insights.

---

## Visuals of Indian Stock Option Analyzer

![Indian Stock Option Analyzer](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdTJoYTNqZnhsYWluODFxZ3Y2ZjR3bDcwdW41ZzYyb2hnd3J6dnZkcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/tSe15uoNuxa9MwtPNR/giphy.gif)
---

## 🚀 Features

- 🔍 Fetch real-time option chain data using the Upstox API
- 📊 Display critical metrics including:
  - Option Greeks (Delta, Gamma, Theta, Vega, Rho)
  - Strike Prices
  - Open Interest (OI)
  - Current Price
- 🤖 Analyze data using Groq API to get:
  - Buy/Sell recommendations
  - Profit percentage projections
  - Risk-reward assessment
- 📁 Easy-to-navigate interface built using Streamlit
- 📈 Designed for quick and intuitive option analysis

---

## 🧠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **APIs Used:**
  - [Upstox API](https://upstox.com) – for real-time market data and masterlist
  - [Groq API](https://groq.com) – for analyzing market data and providing recommendations

---

## 📂 Folder Structure

```plaintext
Indian_Stock_Option_Analyzer/
│
├── upstox_api/               # Folder for Upstox API integration
│   └── (authentication, data fetching scripts)
│
├── Home.py                   # Main entry point for Streamlit app
├── requirements.txt          # Python dependencies
│
├── pages/                                     # Streamlit multipage app folder
│   ├── 1_Phase_1_Select_Option.py             # First stage of option analysis
│   └── 2_Phase_2_Analyze_Option.py            # Final recommendation and evaluation


## Installation

### Clone the Repository
```sh
git clone https://github.com/irikaishani/Indian_Stock_Option_Analyzer.git
cd Indian_Stock_Option_Analyzer
```

### Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Setup API Key
* Get your API credentials from the Upstox Developer Console

* Configure your Groq API key

* Save them in a .env file or Python config file, depending on your implementation

* Create a .env file in the project root:

```sh
UPSTOX_API_KEY=your_upstox_api_key
UPSTOX_API_SECRET=your_upstox_api_secret
UPSTOX_ACCESS_TOKEN=your_upstock_api_accesstoken
GROQ_API_KEY=your_groq_api_key

```

### Start the Application
```sh
streamlit run app.py
```
