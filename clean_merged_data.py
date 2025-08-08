import pandas as pd

# Load the merged dataset
merged_data = pd.read_csv('cleaned_and_merged_housing_data_final.csv')

# Step 1: Remove duplicate rows
merged_data.drop_duplicates(inplace=True)

# Step 2: Consolidate overlapping columns
if 'area_x' in merged_data.columns and 'area_y' in merged_data.columns:
    merged_data['area'] = merged_data['area_x'].combine_first(merged_data['area_y'])
    merged_data.drop(columns=['area_x', 'area_y'], inplace=True)

if 'address_x' in merged_data.columns and 'address_y' in merged_data.columns:
    merged_data['address'] = merged_data['address_x'].combine_first(merged_data['address_y'])
    merged_data.drop(columns=['address_x', 'address_y'], inplace=True)

# Step 3: Drop the `state` column
if 'state' in merged_data.columns:
    merged_data.drop(columns=['state'], inplace=True)

# Step 4: Handle missing values
# Fill numerical columns with median
for col in merged_data.select_dtypes(include=['float64', 'int64']).columns:
    merged_data[col] = merged_data[col].fillna(merged_data[col].median())

# Fill categorical columns with "unknown"
for col in merged_data.select_dtypes(include=['object']).columns:
    merged_data[col] = merged_data[col].fillna("unknown")

# Step 5: Drop sparsely populated columns (threshold: less than 10% non-null)
threshold = 0.1 * len(merged_data)
merged_data = merged_data.loc[:, merged_data.notnull().sum(axis=0) > threshold]

# Step 6: Standardize column names
merged_data.columns = merged_data.columns.str.lower().str.strip().str.replace(" ", "_").str.replace("-", "_")

# Step 7: Validate the refined dataset
print("Refined Dataset Summary:")
print(merged_data.info())

# Save the refined dataset
merged_data.to_csv('refined_cleaned_and_merged_housing_data_final.csv', index=False)
print("Refined dataset saved as 'refined_cleaned_and_merged_housing_data_final.csv'.")

# Optional: Display preview of the refined dataset
print(merged_data.head())
