import requests
import pandas as pd
from bs4 import BeautifulSoup
import pdfplumber

# Function to Fetch and process API Data for Housing Trends from API endpoint
def fetch_api_housing_trends():
    # API url
    url = "https://zillow-com4.p.rapidapi.com/properties/zestimate-history"

    # this zpid is extracted from an API ("https://zillow-com4.p.rapidapi.com/properties/search")
    zpid = ['58335639', '68577093', '45571441', '47093377', '43200418', '43744295', '66762484', '44656581',
            '46926606', '53472961', '48026875', '337594317', '46646294', '47379823', '306011078', '43282469',
            '47050101', '43503111', '103481209', '42832832', '47843712', '43046573', '45896819', '43456080',
            '103370810', '54470064', '47722365']
    # the zpid corresponds to the cities list.
    cities = [
        "Orlando, FL", "Tampa, FL", "Tallahassee, FL",
        "St. Petersburg, FL", "Fort Lauderdale, FL", "Naples, FL", "Sarasota, FL",
        "Pensacola, FL", "West Palm Beach, FL", "Gainesville, FL", "Daytona Beach, FL",
        "Fort Myers, FL", "Boca Raton, FL", "Lakeland, FL", "Cape Coral, FL",
        "Hollywood, FL", "Clearwater, FL", "Palm Bay, FL", "Delray Beach, FL",
        "Coral Springs, FL", "Port St. Lucie, FL", "Pompano Beach, FL", "Ocala, FL",
        "Melbourne, FL", "Bonita Springs, FL", "Sanford, FL", "Winter Park, FL",
    ]

    headers = {
        "x-rapidapi-key": "0b4fa0609bmsh0327918d748d601p17c00djsn36a4948697b4",
        "x-rapidapi-host": "zillow-com4.p.rapidapi.com"
    }

    all_data = []

    for idx, id in enumerate(zpid):
        querystring = {"zpid": id}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        city = cities[idx]

        if "data" in data:
            for chart_data in data["data"].get("homeValueChartData", []):
                for point in chart_data.get("points", []):
                    price = point.get("value")
                    year = point.get("date")
                    all_data.append({
                        "City": city,
                        "Years": year,
                        "Property Value": price
                    })

    # returning a DataFrame for api
    return pd.DataFrame(all_data)


# function for Loading and cleaning Housing data from CSV file
def clean_csv_housing_data(file_name):
    df_csv = pd.read_csv(file_name)

    # selecting dataFrame just for Florida
    df_clean_csv = df_csv[df_csv["State"] == "FL"]

    # Selecting relevant column and standardize names
    df_clean_csv = df_clean_csv[['City', 'Zipcode', 'RentEstimate', 'Area', 'MarketEstimate']].rename(
        columns={'Zipcode': 'zip', 'RentEstimate': 'rent', 'MarketEstimate': 'market_estimate'}
    )
    # Handling the null values
    df_clean_csv = df_clean_csv.fillna("unknown")
    # converting the zipcode column from float to integer
    if "Zipcode" in df_clean_csv.columns:
        df_clean_csv["Zipcode"] = df_clean_csv["Zipcode"].fillna(0).astype(int)

    # returning the dataframe
    return df_clean_csv

# Function for loading and cleaning Rental data from CSV
def clean_rental_data(file_path):
    df = pd.read_csv(file_path)

    # Filter for Florida cities: Osceola and Charlotte
    florida_df = df[df['City'].isin(['KISSIMMEE', 'Saint Cloud', 'PORT CHARLOTTE'])]

    # Select only the relevant columns
    relevant_columns = ['Address', 'City', 'Zip', 'Rent', 'Beds', 'Baths', 'Area', 'Property_Type', 'Price_Per_SqFt',
                        'Year_Built', 'Neighborhood']
    florida_df = florida_df[relevant_columns]

    # Handling missing row data with missing rent values
    florida_df = florida_df.dropna(subset=['Rent'])

    # Standardize column names
    florida_df.columns = florida_df.columns.str.strip().str.lower().str.replace(' ', '_')

    #returning the DataFrame
    return florida_df

# Function to extract rental listings and description by web scraping www.redfin.com website
def scrape_web_data():
    web_url = "https://www.redfin.com/state/Florida/apartments-for-rent"
    web_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en,en-US;q=0.9",
        "cache-control": "max-age=0",
        "priority": "u=0, i",
        "referer": "https://www.redfin.com/rentals",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    data = []
    for page in range(1, 20):
        url = f"{web_url}/page-{page}"
        response = requests.get(url, headers=web_headers)

        # parsing the response using BeautifulSoup
        soup = BeautifulSoup(response.text, features="html.parser")

        # extracting the block that contains all the details
        card = soup.find_all("div", class_="bp-Homecard__Content bp-Homecard__Content--custom")

        for value in card:
            # extracting address HTML elements and getting its text values
            address_div = value.find("div", class_="bp-Homecard__Address--address text-ellipsis")
            address = address_div.get_text(strip=True) if address_div else None

            # extracting description HTML elements and getting its text values
            outer_div = value.find("div", class_="KeyFactsExtension")
            # extract span within the parent div
            description_span = value.find_all("span", class_="KeyFacts-item") if outer_div else []
            description = " | ".join(span.get_text(strip=True) for span in description_span)

            # extracting phone number
            phonenum_button = value.find("button",
                                         class_="bp-Button RentalCTAContact__button RentalCTAContact__button--phone bp-Button__type--ghost bp-Button__size--compact")
            contact = None
            if phonenum_button:
                phone_span = phonenum_button.find("span", class_="ButtonLabel")
                contact = phone_span.get_text(strip=True) if phone_span else None

            price_div = value.find("div",
                                   class_="bp-Homecard__SmallestUnit flex flex-grow flex-wrap align-baseline color-text-primary font-headline-xsmall")
            price = price_div.get_text(strip=True) if price_div else None

            data.append({
                "Address": address,
                "Rental Price": price,
                "Description of the Rental Space": description,
                "Contact": contact
            })
    # returning the DataFrame
    return pd.DataFrame(data)


# Function to load and extract household demographic data from Excel file
def extract_household_data(file_path):
    # Load the 'Data' sheet
    df = pd.read_excel(file_path, sheet_name='Data', skiprows=2)

    # Focus on relevant columns
    df = df.iloc[:, [0, 1, 3, 5, 7, 9]]  # Columns: Label, Total, Married-couple, Male, Female, Nonfamily
    df.columns = [
        'Label',
        'Total_Households',
        'Married_Couple',
        'Male_Householder',
        'Female_Householder',
        'Nonfamily_Household'
    ]

    # Drop rows with NaN labels
    df = df.dropna(subset=['Label'])

    # Clean up columns
    for col in df.columns[1:]:
        df[col] = df[col].str.replace(",", "").str.replace("±.*", "").str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Filter relevant labels
    relevant_labels = [
        'Total households',
        'Average household size',
        'Total families',
        'Married-couple family household',
        'Male householder, no spouse present',
        'Female householder, no spouse present',
        'Nonfamily household'
    ]
    df = df[df['Label'].isin(relevant_labels)]

    # Pivot the data for easier integration
    df = df.set_index('Label').T.reset_index()
    df.rename(columns={'index': 'Category'}, inplace=True)

    return df

# Function to load and extract household ownership data from PDF

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
        if len(parts) > 7:  # Ensuring the line has at least the expected number of parts
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
    # returning the DataFrame
    return df

# Function to handle merging and cleaning of the data.
def process_and_clean_data():
    # Load datasets
    housing_trends_df = fetch_api_housing_trends()
    rental_price_df = scrape_web_data()
    housing_policy_df = extract_homeownership_data("housing_policy_fl.pdf")
    florida_rental_cleaned_df = clean_rental_data("rental_countyraw_data.csv")
    household_data_df = extract_household_data("ACSST1Y2023.S1101-2024-12-07T234848.xlsx")
    cleaned_data_df = clean_csv_housing_data("housing_data.csv")

    # Standardize column names
    for df in [housing_trends_df, rental_price_df, housing_policy_df, florida_rental_cleaned_df, household_data_df, cleaned_data_df]:
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_").str.replace("-", "_")

    # Rename and align key columns
    if "zipcode" in cleaned_data_df.columns:
        cleaned_data_df.rename(columns={"zipcode": "zip"}, inplace=True)
    if "county" in housing_policy_df.columns:
        housing_policy_df.rename(columns={"county": "city"}, inplace=True)

    # Ensure 'zip' and 'city' columns are consistent
    for df in [cleaned_data_df, florida_rental_cleaned_df, rental_price_df]:
        if "zip" in df.columns:
            df["zip"] = df["zip"].astype(str).str.zfill(5)
        if "city" in df.columns:
            df["city"] = df["city"].str.lower()

    # Process `housing_trends_df` to match other datasets
    city_columns = [col for col in housing_trends_df.columns if col.endswith("_price")]
    housing_trends_long = housing_trends_df.melt(id_vars="years", value_vars=city_columns,
                                                 var_name="city", value_name="trend_property_value")
    housing_trends_long["city"] = housing_trends_long["city"].str.replace("_price", "").str.replace(",", "").str.lower()

    # Extract `city` from `rental_price_df` address
    if "address" in rental_price_df.columns:
        rental_price_df["city"] = rental_price_df["address"].str.extract(r",\s*([^,]+),\s*fl")[0].str.lower()

    # Ensure 'years' column consistency
    if "years" in housing_trends_long.columns:
        housing_trends_long.rename(columns={"years": "year"}, inplace=True)

    # Incrementally merge datasets
    merged_df = cleaned_data_df.merge(florida_rental_cleaned_df, on=["city", "zip"], how="outer")
    merged_df = merged_df.merge(housing_policy_df, on="city", how="outer")
    merged_df = merged_df.merge(rental_price_df, on="city", how="outer")
    if "year" in housing_trends_long.columns and "year" in merged_df.columns:
        merged_df = merged_df.merge(housing_trends_long, on=["city", "year"], how="outer")

    # Adding calculated fields
    if "marketestimate" in merged_df.columns and "total_households" in merged_df.columns:
        merged_df["price_to_income_ratio"] = merged_df["marketestimate"] / merged_df["total_households"]

    if "rent" in merged_df.columns and "area" in merged_df.columns:
        merged_df["average_rent_per_sqft"] = merged_df["rent"] / merged_df["area"]

    # Refining the merged dataset
    merged_df.drop_duplicates(inplace=True)
    if 'area_x' in merged_df.columns and 'area_y' in merged_df.columns:
        merged_df['area'] = merged_df['area_x'].combine_first(merged_df['area_y'])
        merged_df.drop(columns=['area_x', 'area_y'], inplace=True)

    if 'address_x' in merged_df.columns and 'address_y' in merged_df.columns:
        merged_df['address'] = merged_df['address_x'].combine_first(merged_df['address_y'])
        merged_df.drop(columns=['address_x', 'address_y'], inplace=True)

    if 'state' in merged_df.columns:
        merged_df.drop(columns=['state'], inplace=True)

    # Fill missing values
    for col in merged_df.select_dtypes(include=['float64', 'int64']).columns:
        merged_df[col] = merged_df[col].fillna(merged_df[col].median())
    for col in merged_df.select_dtypes(include=['object']).columns:
        merged_df[col] = merged_df[col].fillna("unknown")

    # Drop sparsely populated columns
    threshold = 0.1 * len(merged_df)
    merged_df = merged_df.loc[:, merged_df.notnull().sum(axis=0) > threshold]

    # Standardize column names
    merged_df.columns = merged_df.columns.str.lower().str.strip().str.replace(" ", "_").str.replace("-", "_")

    # Save the refined dataset
    merged_df.to_csv('Merger_cleaned_Prepared_data_for_Florida_by_group_9.csv', index=False)
    print("Dataset saved as 'Merger_cleaned_Prepared_data_for_Florida_by_group_9.csv'.")

process_and_clean_data()
