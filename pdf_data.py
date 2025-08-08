import pdfplumber
import pandas as pd

def extract_homeownership_data(pdf_path, start_page=32, end_page=39):
    # Extract text from specified pages
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(start_page - 1, end_page):  # Pages are 0-indexed in pdfplumber
            page = pdf.pages[page_num]
            text = page.extract_text()
            if text:
                lines.extend(text.split("\n"))

    # Define the expected columns
    columns = [
        "County", "Households_Served_First_Mortgage", "First_Mortgage",
        "DPA", "Average_Sales_Price", "Households_Served_DPA",
        "DPA_Amount", "DPA_Sales_Price"
    ]

    # Process lines to extract data
    structured_data = []
    for line in lines:
        # Skip empty or malformed lines
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) > 7:  # Ensure the line has at least the expected number of parts
            try:
                county = parts[0]
                households_served_first_mortgage = int(parts[1].replace(",", ""))
                first_mortgage = float(parts[2].replace(",", "").replace("$", ""))
                dpa = float(parts[3].replace(",", "").replace("$", ""))
                avg_sales_price = float(parts[4].replace(",", "").replace("$", ""))
                households_served_dpa = int(parts[5].replace(",", ""))
                dpa_amount = float(parts[6].replace(",", "").replace("$", ""))
                dpa_sales_price = float(parts[7].replace(",", "").replace("$", ""))

                # Append the structured row
                structured_data.append([
                    county, households_served_first_mortgage, first_mortgage, dpa,
                    avg_sales_price, households_served_dpa, dpa_amount, dpa_sales_price
                ])
            except (ValueError, IndexError):
                # Skip lines that do not match the expected format
                continue

    # Convert to DataFrame
    df = pd.DataFrame(structured_data, columns=columns)

    # Remove rows where 'County' is "TOTALS"
    df = df[df["County"].str.strip().str.upper() != "TOTALS"]

    return df

# Usage
pdf_path = "housing_policy_fl.pdf"
df_homeownership = extract_homeownership_data(pdf_path)

# Save the cleaned data to a CSV file


# Display the first few rows of the cleaned DataFrame
print(df_homeownership)
