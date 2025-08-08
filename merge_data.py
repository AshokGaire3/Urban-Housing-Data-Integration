def process_and_clean_data():
    import pandas as pd

    # Load datasets
    housing_trends_df = pd.read_csv('HousingTrends.csv')
    rental_price_df = pd.read_csv('Rental_Price.csv')
    housing_policy_df = pd.read_csv('housing_policy.csv')
    florida_rental_cleaned_df = pd.read_csv('florida_rental_data_cleaned.csv')
    household_data_df = pd.read_csv('household_data.csv')
    cleaned_data_df = pd.read_csv('cleaned_data.csv')

    # Step 1: Standardize column names
    for df in [housing_trends_df, rental_price_df, housing_policy_df, florida_rental_cleaned_df, household_data_df, cleaned_data_df]:
        df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_").str.replace("-", "_")

    # Step 2: Rename and align key columns
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

    # Step 3: Process `housing_trends_df` to match other datasets
    city_columns = [col for col in housing_trends_df.columns if col.endswith("_price")]
    housing_trends_long = housing_trends_df.melt(id_vars="years", value_vars=city_columns,
                                                 var_name="city", value_name="property_value")
    housing_trends_long["city"] = housing_trends_long["city"].str.replace("_price", "").str.replace(",", "").str.lower()

    # Step 4: Extract `city` from `rental_price_df` address
    if "address" in rental_price_df.columns:
        rental_price_df["city"] = rental_price_df["address"].str.extract(r",\s*([^,]+),\s*fl")[0].str.lower()

    # Step 5: Ensure 'years' column consistency
    if "years" in housing_trends_long.columns:
        housing_trends_long.rename(columns={"years": "year"}, inplace=True)

    # Step 6: Incrementally merge datasets
    merged_df = cleaned_data_df.merge(florida_rental_cleaned_df, on=["city", "zip"], how="outer")
    merged_df = merged_df.merge(housing_policy_df, on="city", how="outer")
    merged_df = merged_df.merge(rental_price_df, on="city", how="outer")
    if "year" in housing_trends_long.columns and "year" in merged_df.columns:
        merged_df = merged_df.merge(housing_trends_long, on=["city", "year"], how="outer")

    # Step 7: Add calculated fields
    if "marketestimate" in merged_df.columns and "total_households" in merged_df.columns:
        merged_df["price_to_income_ratio"] = merged_df["marketestimate"] / merged_df["total_households"]

    if "rent" in merged_df.columns and "area" in merged_df.columns:
        merged_df["average_rent_per_sqft"] = merged_df["rent"] / merged_df["area"]

    # Step 8: Refine the merged dataset
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
    merged_df.to_csv('refined_cleaned_and_merged_housing_data_final.csv', index=False)
    print("Refined dataset saved as 'refined_cleaned_and_merged_housing_data_final.csv'.")

process_and_clean_data()