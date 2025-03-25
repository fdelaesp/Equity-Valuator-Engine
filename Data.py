import os
import yfinance as yf
import pandas as pd


def collect_financials(ticker_symbol: str):
    """
    Fetches the income statement, balance sheet, and cash flow data for a given ticker.
    """
    ticker = yf.Ticker(ticker_symbol)

    # Pull financial statements from yfinance
    income_stmt = ticker.financials
    balance_sheet = ticker.balance_sheet
    cash_flow = ticker.cashflow

    return income_stmt, balance_sheet, cash_flow


def save_dataframes(ticker_symbol: str, income_stmt: pd.DataFrame,
                    balance_sheet: pd.DataFrame, cash_flow: pd.DataFrame):
    """
    Saves the financial dataframes as CSV files in the data/ folder.
    """
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    income_stmt.to_csv(os.path.join(data_dir, f"{ticker_symbol}_income_statement.csv"))
    balance_sheet.to_csv(os.path.join(data_dir, f"{ticker_symbol}_balance_sheet.csv"))
    cash_flow.to_csv(os.path.join(data_dir, f"{ticker_symbol}_cash_flow.csv"))


def main():
    # Example: Using AAPL, but you can modify to accept dynamic input
    ticker_symbol = input("Enter the ticker symbol (e.g., AAPL): ").strip().upper()

    print(f"Fetching financial data for {ticker_symbol}...")
    income_stmt, balance_sheet, cash_flow = collect_financials(ticker_symbol)

    # Display fetched data (optional)
    print("\nIncome Statement:")
    print(income_stmt.head())
    print("\nBalance Sheet:")
    print(balance_sheet.head())
    print("\nCash Flow Statement:")
    print(cash_flow.head())

    # Save the data to CSV files
    save_dataframes(ticker_symbol, income_stmt, balance_sheet, cash_flow)
    print(f"\nFinancial data for {ticker_symbol} saved in the 'data' directory.")


if __name__ == "__main__":
    main()
