import time

import requests




florida_cities = [
     "Palm Bay, FL", "Delray Beach, FL",
    "Coral Springs, FL", "Port St. Lucie, FL", "Pompano Beach, FL", "Ocala, FL",
    "Melbourne, FL", "Bonita Springs, FL", "Sanford, FL", "Winter Park, FL",

]


url = "https://zillow-com4.p.rapidapi.com/properties/search"

querystring = {"location":"Houston, TX","status":"forSale","sort":"relevance","sortType":"asc","priceType":"listPrice","listingType":"agent"}

headers = {
	"x-rapidapi-key": "49b8f6e073mshce95b3c39357a85p116550jsn5954e956d7bb",
	"x-rapidapi-host": "zillow-com4.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

list_zip = []
for city in florida_cities:
    querystring = {
        "location": city,
        "status": "forSale",
        "sort": "relevance",
        "sortType": "asc",
        "priceType": "listPrice",
        "listingType": "agent"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        if data and data.get("data") and isinstance(data["data"], list) and len(data["data"]) > 0 and data["data"][0].get("zpid"):
            list_zip.append(data["data"][0]["zpid"])
        else:
            print(f"No data or unexpected format for {city}: {data}")


        # Implement more robust rate limiting here if necessary
        time.sleep(2)  # Reduced sleep time for demonstration

    except requests.exceptions.RequestException as e:
        print(f"Error requesting data for {city}: {e}")
    except (KeyError, IndexError) as e:
        print(f"Error parsing data for {city}: {e}")


print(list_zip)