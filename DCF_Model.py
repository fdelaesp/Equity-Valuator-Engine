import numpy as np
import numpy_financial as npf


def calculate_fcf(ebit, tax_rate, da, capex, wc):
    """
    Calculate Free Cash Flow (FCF) from EBIT, accounting for taxes, depreciation/amortization,
    capital expenditures, and working capital changes.

    Parameters:
        ebit (float): Earnings Before Interest and Taxes.
        tax_rate (float): Effective tax rate (e.g., 0.21 for 21%).
        da (float): Depreciation & Amortization.
        capex (float): Capital Expenditures.
        wc (float): Net change in Working Capital.

    Returns:
        float: Free Cash Flow value.
    """
    nopat = ebit * (1 - tax_rate)
    return nopat + da - capex - wc


def project_fcf(initial_fcf, growth_rate, years):
    """
    Project future Free Cash Flows given a base FCF and a constant growth rate.

    Parameters:
        initial_fcf (float): Base year FCF.
        growth_rate (float): Annual growth rate (e.g., 0.05 for 5%).
        years (int): Number of years to project.

    Returns:
        list: Projected FCFs for each year.
    """
    return [initial_fcf * ((1 + growth_rate) ** i) for i in range(1, years + 1)]


def calculate_terminal_value(last_fcf, perpetual_growth_rate, wacc):
    """
    Calculate the terminal value using the perpetuity growth method.

    Parameters:
        last_fcf (float): The final year's projected FCF.
        perpetual_growth_rate (float): Perpetual growth rate after projection period.
        wacc (float): Weighted Average Cost of Capital (discount rate).

    Returns:
        float: Terminal value.
    """
    return last_fcf * (1 + perpetual_growth_rate) / (wacc - perpetual_growth_rate)


def discount_cash_flows(cash_flows, wacc):
    """
    Discount a series of cash flows back to present value using the WACC.
    The cash flows should start at period 1.

    Parameters:
        cash_flows (list): List of future cash flows.
        wacc (float): Discount rate.

    Returns:
        float: Sum of the present values of the cash flows.
    """
    # npf.npv assumes cash flows from period 1 onward
    return npf.npv(wacc, cash_flows)


def calculate_dcf(ebit, tax_rate, da, capex, wc, growth_rate, projection_years, perpetual_growth_rate, wacc):
    """
    Compute the Discounted Cash Flow (DCF) value of a company.

    Steps:
      1. Calculate base FCF.
      2. Project FCF for a set number of years.
      3. Compute terminal value using the final projected FCF.
      4. Discount projected FCFs and terminal value back to present value.

    Parameters:
        ebit (float): Current EBIT.
        tax_rate (float): Effective tax rate.
        da (float): Depreciation & Amortization.
        capex (float): Capital Expenditures.
        wc (float): Net change in Working Capital.
        growth_rate (float): Annual growth rate for projecting FCF.
        projection_years (int): Number of years to forecast.
        perpetual_growth_rate (float): Growth rate for terminal value calculation.
        wacc (float): Discount rate (Weighted Average Cost of Capital).

    Returns:
        tuple:
            total_value (float): Enterprise value based on DCF.
            fcf_projections (list): List of projected FCFs.
            terminal_value (float): Calculated terminal value.
    """
    # Step 1: Base year FCF
    base_fcf = calculate_fcf(ebit, tax_rate, da, capex, wc)

    # Step 2: Project FCF over the forecast period
    fcf_projections = project_fcf(base_fcf, growth_rate, projection_years)

    # Step 3: Calculate terminal value using the final projected FCF
    terminal_value = calculate_terminal_value(fcf_projections[-1], perpetual_growth_rate, wacc)

    # Discount each projected FCF and the terminal value to present value
    discounted_fcf = [fcf / ((1 + wacc) ** (i + 1)) for i, fcf in enumerate(fcf_projections)]
    discounted_terminal = terminal_value / ((1 + wacc) ** (projection_years + 1))

    total_value = sum(discounted_fcf) + discounted_terminal
    return total_value, fcf_projections, terminal_value


if __name__ == "__main__":
    # Example assumptions (units can be in millions or any consistent scale)
    ebit = 1000.0  # Current EBIT
    tax_rate = 0.21  # 21% effective tax rate
    da = 100.0  # Depreciation & Amortization
    capex = 150.0  # Capital Expenditures
    wc = 50.0  # Working Capital change
    growth_rate = 0.05  # 5% annual growth in FCFs
    projection_years = 5  # Forecast horizon (years)
    perpetual_growth_rate = 0.02  # Terminal (perpetual) growth rate of 2%
    wacc = 0.08  # 8% discount rate

    dcf_value, fcf_projections, term_value = calculate_dcf(
        ebit, tax_rate, da, capex, wc,
        growth_rate, projection_years, perpetual_growth_rate, wacc
    )

    print("DCF Enterprise Value:", round(dcf_value, 2))
    print("Projected FCFs:", [round(f, 2) for f in fcf_projections])
    print("Terminal Value:", round(term_value, 2))
