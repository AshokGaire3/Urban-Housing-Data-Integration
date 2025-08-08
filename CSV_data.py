import pandas as pd

file_name = "housing_data.csv"
df_csv = pd.read_csv(file_name)

# selecting dataFrame just for Florida
df_clean_csv = df_csv[df_csv["State"]=="FL"]

# Dropping unnecessary data
df_clean_csv = df_clean_csv.drop(["PPSq","LotArea","Latitude","Longitude"],axis="columns")

# Handling the null values
df_clean_csv = df_clean_csv.fillna("null")

if "Zipcode" in df_clean_csv.columns:
    df_clean_csv["Zipcode"] = df_clean_csv["Zipcode"].fillna(0).astype(int)

#converting the cleaned dataFrame to CSV
df_clean_csv.to_csv("cleaned_data.csv", index=False)










