import streamlit as st
import numpy as np
import os

# Import your modules
from DCF_Model import calculate_dcf
from Models import run_lbo_model
from Comps_Model import compute_median_multiple, apply_comps
from Excel import export_dcf_results
from Data import collect_financials, save_dataframes

# Set page configuration and title
st.set_page_config(page_title="Equity Valuation Engine", layout="wide")
st.title("Equity Valuation Engine Dashboard")

# Sidebar: Choose valuation method
valuation_method = st.sidebar.selectbox(
    "Select Valuation Method",
    [
        "Discounted Cash Flow (DCF)",
        "Comparable Companies (Comps)",
        "Leveraged Buyout (LBO)",
        "Data Collection"
    ]
)

if valuation_method == "Discounted Cash Flow (DCF)":
    st.header("Discounted Cash Flow (DCF) Valuation")
    st.subheader("Input Assumptions")

    ebit = st.number_input("EBIT", value=1000.0)
    tax_rate = st.number_input("Tax Rate (%)", value=21.0) / 100.0
    da = st.number_input("Depreciation & Amortization", value=100.0)
    capex = st.number_input("Capital Expenditures", value=150.0)
    wc = st.number_input("Net Change in Working Capital", value=50.0)
    growth_rate = st.number_input("FCF Growth Rate (%)", value=5.0) / 100.0
    projection_years = st.number_input("Projection Years", value=5, step=1)
    perpetual_growth_rate = st.number_input("Terminal Growth Rate (%)", value=2.0) / 100.0
    wacc = st.number_input("WACC (%)", value=8.0) / 100.0

    if st.button("Calculate DCF"):
        dcf_value, fcf_projections, terminal_value = calculate_dcf(
            ebit, tax_rate, da, capex, wc,
            growth_rate, projection_years, perpetual_growth_rate, wacc
        )
        st.success(f"DCF Enterprise Value: {dcf_value:.2f}")
        st.write("Projected Free Cash Flows:", fcf_projections)
        st.write("Terminal Value:", terminal_value)
        st.line_chart(fcf_projections)

        if st.button("Export DCF Results to Excel"):
            output_file = "outputs/dcf_results.xlsx"
            export_dcf_results(output_file, fcf_projections, terminal_value, dcf_value)
            st.info(f"DCF results exported to {output_file}")

elif valuation_method == "Comparable Companies (Comps)":
    st.header("Comparable Companies (Comps) Valuation")
    st.subheader("Static Peer Group")

    # Static peer data – extend with dynamic data later if needed
    peers = [
        {"ticker": "AAPL", "EV/EBITDA": 18.0},
        {"ticker": "MSFT", "EV/EBITDA": 20.0},
        {"ticker": "GOOGL", "EV/EBITDA": 19.0},
        {"ticker": "AMZN", "EV/EBITDA": 22.0},
        {"ticker": "FB", "EV/EBITDA": 16.0},
    ]
    target_ebitda = st.number_input("Target Company EBITDA", value=150.0)

    if st.button("Calculate Comps"):
        median_ev_ebitda = compute_median_multiple(peers, "EV/EBITDA")
        enterprise_value = apply_comps(target_ebitda, median_ev_ebitda)
        st.success(f"Estimated Enterprise Value: {enterprise_value:.2f}")
        st.write("Median EV/EBITDA Multiple:", median_ev_ebitda)

elif valuation_method == "Leveraged Buyout (LBO)":
    st.header("Leveraged Buyout (LBO) Model")
    st.subheader("Input LBO Assumptions")

    purchase_price = st.number_input("Purchase Price (Enterprise Value)", value=1000.0)
    debt_ratio = st.number_input("Debt Ratio (e.g., 0.6)", value=0.6)
    initial_ebitda = st.number_input("Initial EBITDA", value=120.0)
    ebitda_growth_rate = st.number_input("EBITDA Growth Rate (%)", value=5.0) / 100.0
    exit_multiple = st.number_input("Exit EV/EBITDA Multiple", value=8.0)
    years = st.number_input("Projection Years", value=5, step=1)
    interest_rate = st.number_input("Interest Rate on Debt (%)", value=8.0) / 100.0

    if st.button("Calculate LBO"):
        equity_cash_flows, irr, exit_equity_value = run_lbo_model(
            purchase_price,
            debt_ratio,
            initial_ebitda,
            ebitda_growth_rate,
            exit_multiple,
            years,
            interest_rate
        )
        st.success(f"Exit Equity Value: {exit_equity_value:.2f}")
        st.write("Equity Cash Flows:", equity_cash_flows)
        st.write("Equity IRR: {:.2%}".format(irr))
        st.line_chart(equity_cash_flows)

elif valuation_method == "Data Collection":
    st.header("Data Collection")
    tickers = st.multiselect(
        "Select Ticker Symbols",
        options=["AAPL", "MSFT", "GOOGL", "AMZN", "FB"],
        default=["AAPL"]
    )

    if st.button("Fetch Financial Data"):
        for ticker_symbol in tickers:
            income_stmt, balance_sheet, cash_flow = collect_financials(ticker_symbol)
            st.subheader(f"Financial Data for {ticker_symbol}")
            st.write("**Income Statement:**")
            st.write(income_stmt.head())
            st.write("**Balance Sheet:**")
            st.write(balance_sheet.head())
            st.write("**Cash Flow Statement:**")
            st.write(cash_flow.head())

    if st.button("Save Data to CSV"):
        for ticker_symbol in tickers:
            # Re-fetch data for each ticker (you can cache these results to avoid multiple calls)
            income_stmt, balance_sheet, cash_flow = collect_financials(ticker_symbol)
            save_dataframes(ticker_symbol, income_stmt, balance_sheet, cash_flow)
        st.info(f"Financial data for {', '.join(tickers)} saved in the 'data' directory.")

# Launch the Streamlit server automatically if run without extra arguments.
if __name__ == "__main__":
    import sys, subprocess

    if len(sys.argv) == 1 and os.getenv("MY_STREAMLIT_LAUNCHED") is None:
        os.environ["MY_STREAMLIT_LAUNCHED"] = "1"
        subprocess.run([sys.executable, "-m", "streamlit", "run", __file__])
        sys.exit()
