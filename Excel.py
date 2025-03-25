import os
import xlsxwriter


def export_dcf_results(filename, fcf_projections, terminal_value, dcf_enterprise_value):
    """
    Exports DCF model outputs to an Excel file.

    Parameters:
        filename (str): The output Excel file path.
        fcf_projections (list): List of projected Free Cash Flows (one per year).
        terminal_value (float): Calculated terminal value.
        dcf_enterprise_value (float): Total DCF enterprise value.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Create a new Excel workbook and add a worksheet
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet("DCF Results")

    # Write headers
    worksheet.write("A1", "Year")
    worksheet.write("B1", "Projected FCF")

    # Write projected FCFs for each forecast year
    for i, fcf in enumerate(fcf_projections, start=1):
        worksheet.write(i, 0, i)  # Year (starting at 1)
        worksheet.write(i, 1, fcf)  # FCF for that year

    # Write terminal value and overall DCF enterprise value
    start_row = len(fcf_projections) + 2
    worksheet.write(start_row, 0, "Terminal Value")
    worksheet.write(start_row, 1, terminal_value)
    worksheet.write(start_row + 1, 0, "DCF Enterprise Value")
    worksheet.write(start_row + 1, 1, dcf_enterprise_value)

    # Close the workbook to save the file
    workbook.close()


if __name__ == "__main__":
    # Example DCF results (adjust these values as needed)
    fcf_projections = [100, 105, 110, 115, 120]  # Projected FCFs for 5 years
    terminal_value = 1500  # Calculated terminal value
    dcf_enterprise_value = 2000  # Total enterprise value from DCF

    output_file = "outputs/dcf_results.xlsx"
    export_dcf_results(output_file, fcf_projections, terminal_value, dcf_enterprise_value)
    print(f"DCF results exported to {output_file}")
