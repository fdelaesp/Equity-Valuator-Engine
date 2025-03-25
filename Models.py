import numpy as np
import numpy_financial as npf


def run_lbo_model(purchase_price: float,
                  debt_ratio: float,
                  initial_ebitda: float,
                  ebitda_growth_rate: float,
                  exit_multiple: float,
                  years: int,
                  interest_rate: float):
    """
    Run a simplified Leveraged Buyout (LBO) model.

    Assumptions:
      - The target is purchased at an enterprise value (purchase_price).
      - Financing is split between debt and equity according to debt_ratio.
      - Debt is repaid on a constant schedule over the projection period.
      - EBITDA grows at a constant rate.
      - Exit value is computed as (exit_multiple * final EBITDA).
      - No interim cash distributions are assumed; equity returns come from the exit.

    Parameters:
      purchase_price (float): Enterprise value at purchase.
      debt_ratio (float): Fraction of the purchase financed with debt (e.g., 0.6 for 60% debt).
      initial_ebitda (float): Current EBITDA of the target.
      ebitda_growth_rate (float): Annual growth rate for EBITDA (e.g., 0.05 for 5%).
      exit_multiple (float): Exit EV/EBITDA multiple at sale.
      years (int): Projection horizon (typically 5 years).
      interest_rate (float): Annual interest rate on outstanding debt.

    Returns:
      tuple:
        equity_cash_flows (list): Series of equity cash flows (time 0 investment and final exit).
        irr (float): Internal Rate of Return (IRR) for the equity investment.
        exit_equity_value (float): The estimated equity value at exit.
    """
    # Initial financing
    equity_investment = purchase_price * (1 - debt_ratio)
    initial_debt = purchase_price * debt_ratio

    # Assume constant principal repayment over the projection period
    annual_principal_payment = initial_debt / years
    outstanding_debt = initial_debt

    # Simulate debt repayment over the projection period (interest accrues each year)
    debt_schedule = []
    for year in range(1, years + 1):
        interest_expense = outstanding_debt * interest_rate
        # For a more detailed model, one might subtract available free cash flow here.
        # For this basic example, we assume fixed annual principal repayments.
        outstanding_debt -= annual_principal_payment
        debt_schedule.append({
            "year": year,
            "interest_expense": interest_expense,
            "principal_payment": annual_principal_payment,
            "remaining_debt": max(outstanding_debt, 0)
        })

    # Project EBITDA over the horizon
    final_ebitda = initial_ebitda * ((1 + ebitda_growth_rate) ** years)

    # Estimate exit enterprise value using the exit multiple
    exit_enterprise_value = exit_multiple * final_ebitda

    # At exit, the remaining debt (ideally zero or minimal if fully repaid) is subtracted to get equity value.
    exit_equity_value = exit_enterprise_value - max(outstanding_debt, 0)

    # For this simplified model, assume no interim equity distributions.
    # Equity cash flows: initial negative investment at time 0 and exit value at final year.
    equity_cash_flows = [-equity_investment] + [0] * (years - 1) + [exit_equity_value]

    # Calculate the IRR for the equity investors.
    irr = npf.irr(equity_cash_flows)

    return equity_cash_flows, irr, exit_equity_value


if __name__ == "__main__":
    # Example assumptions:
    purchase_price = 1000.0  # Enterprise value at purchase
    debt_ratio = 0.6  # 60% of the purchase is financed with debt
    initial_ebitda = 120.0  # Starting EBITDA
    ebitda_growth_rate = 0.05  # 5% annual growth in EBITDA
    exit_multiple = 8.0  # Exit EV/EBITDA multiple
    years = 5  # Projection period (years)
    interest_rate = 0.08  # Annual interest rate on debt

    equity_cash_flows, irr, exit_equity_value = run_lbo_model(
        purchase_price,
        debt_ratio,
        initial_ebitda,
        ebitda_growth_rate,
        exit_multiple,
        years,
        interest_rate
    )

    print("Equity Cash Flows:", equity_cash_flows)
    print("Exit Equity Value:", round(exit_equity_value, 2))
    print("Equity IRR: {:.2%}".format(irr))
