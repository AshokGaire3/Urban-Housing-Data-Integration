import pandas as pd

# Load the dataset
file_path = 'rental_countyraw_data.csv'  # Replace with the actual path
df = pd.read_csv(file_path)

# Filter for Florida cities: Osceola and Charlotte
florida_df = df[df['City'].isin(['KISSIMMEE', 'Saint Cloud','PORT CHARLOTTE'])]

# Select only the relevant columns
relevant_columns = ['Address','City','Zip', 'Rent', 'Beds', 'Baths', 'Area','Property_Type', 'Price_Per_SqFt', 'Year_Built', 'Neighborhood']
florida_df = florida_df[relevant_columns]

# Check for missing values
print(florida_df.isnull().sum())

# Handle missing data (example: drop rows with missing rent data)
florida_df = florida_df.dropna(subset=['Rent'])

# Standardize column names (optional)
florida_df.columns = florida_df.columns.str.strip().str.lower().str.replace(' ', '_')

# Check the cleaned dataset
print(florida_df.head())

# Save the cleaned data if needed
florida_df.to_csv('florida_rental_data_cleaned.csv', index=False)
