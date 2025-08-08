import requests
import pandas as pd

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
    "Pensacola, FL","West Palm Beach, FL", "Gainesville, FL", "Daytona Beach, FL",
    "Fort Myers, FL", "Boca Raton, FL", "Lakeland, FL", "Cape Coral, FL",
    "Hollywood, FL", "Clearwater, FL", "Palm Bay, FL", "Delray Beach, FL",
    "Coral Springs, FL", "Port St. Lucie, FL", "Pompano Beach, FL", "Ocala, FL",
    "Melbourne, FL", "Bonita Springs, FL", "Sanford, FL", "Winter Park, FL",
]

headers = {
	"x-rapidapi-key": "49b8f6e073mshce95b3c39357a85p116550jsn5954e956d7bb",
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

# Creating a DataFrame
df = pd.DataFrame(all_data)

# handling the duplicates rows
df_aggregated = df.groupby(['Years', 'City'], as_index=False).mean()

#pivot data for cities as separate columns
pivoted_df = df_aggregated.pivot(index='Years', columns='City', values='Property Value')

# flattening the MultiIndex for better readability
pivoted_df.columns = [f"{city}_Price" for city in pivoted_df.columns]

# Reset index to include 'Years' as a regular column
pivoted_df.reset_index(inplace=True)

#replacing the NaN values with "not available"
pivoted_df.astype(object).fillna("not available", inplace=True)

# Save transformed data to CSV without index
pivoted_df.to_csv("HousingTrends.csv", index=False)
print("Housing Trends CSV file created.")
