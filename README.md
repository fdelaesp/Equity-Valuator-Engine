# Equity-Valuator-Engine
A modular equity valuation engine featuring DCF, Comparable Company Analysis, and LBO modeling, with integrated financial data collection from Yahoo Finance and an interactive Streamlit dashboard.



# 📊 Equity Valuation Engine

A modular Python application for valuing stocks using **Discounted Cash Flow (DCF)**, **Comparable Company Analysis (Comps)**, and **Leveraged Buyout (LBO)** methodologies — complete with a Streamlit dashboard and live data integration from Yahoo Finance.

---

## 🚀 Features

- ✅ **DCF Model**: Project Free Cash Flows, apply WACC, and calculate terminal value  
- ✅ **Comps Model**: Apply valuation multiples from comparable companies  
- ✅ **LBO Model**: Run 5-year IRR scenarios with leverage assumptions  
- ✅ **Live Data Fetching**: Pull income statement, balance sheet, and cash flow data via `yfinance`  
- ✅ **Multi-Ticker Support**: Analyze multiple stocks simultaneously  
- ✅ **Interactive UI**: Intuitive Streamlit dashboard  
- ✅ **Excel Export**: Export clean analyst-style outputs to `.xlsx`

---

## 🧱 Project Structure

```
EquityValuationEngine/
├── data/                 # Raw financial data (downloaded or cached)
├── models/               # Core modeling logic
│   ├── dcf.py            # Discounted Cash Flow logic
│   ├── comps.py          # Comparable Company Analysis
│   └── lbo.py            # Leveraged Buyout model
├── outputs/              # Excel or CSV exports
├── utils/                # Helper functions (e.g., WACC calculator)
├── dashboard.py          # Streamlit interface
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🧪 How to Use

### ▶️ 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
- `streamlit`
- `pandas`
- `yfinance`
- `numpy`
- `numpy-financial`
- `xlsxwriter`

---

### ▶️ 2. Launch the Dashboard

```bash
python dashboard.py
```

> The app will automatically launch in your browser at [http://localhost:8501](http://localhost:8501)

---

### 📈 3. Choose a Valuation Method

Use the sidebar to select:
- **Discounted Cash Flow (DCF)**
- **Comparable Company Analysis (Comps)**
- **Leveraged Buyout (LBO)**
- **Data Collection**

Then input assumptions and fetch financials.

---

### 💾 4. Export to Excel

After running a valuation, click **"Export to Excel"** to save your results in the `/outputs/` directory.

---

## 📚 Example Use Cases

- 📉 Valuing a tech stock using DCF with terminal multiples  
- 🧾 Pulling peer financials and applying EV/EBITDA multiples  
- 💰 Modeling a 5-year leveraged buyout with IRR output  
- 🔍 Collecting financial data for a basket of tickers (AAPL, MSFT, GOOGL, etc.)


---

## 📄 License

MIT License. Free for academic and commercial use with attribution.
