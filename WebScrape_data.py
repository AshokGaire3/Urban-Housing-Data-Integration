from bs4 import BeautifulSoup
import requests
import pandas as pd


web_url= "https://www.redfin.com/state/Florida/apartments-for-rent"
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
for page in range(1,20):
    url = f"{web_url}/page-{page}"
    response = requests.get(url, headers=web_headers)

    # parsing the response using BeautifulSoup
    soup = BeautifulSoup(response.text, features="html.parser")

    # extracting the block that contains all the details
    card = soup.find_all("div", class_="bp-Homecard__Content bp-Homecard__Content--custom")

    for value in card:
        # extracting address HTML elements and getting its text values
        address_div = value.find("div",class_="bp-Homecard__Address--address text-ellipsis")
        address = address_div.get_text(strip=True) if address_div else None

        # extracting description HTML elements and getting its text values
        outer_div = value.find("div",class_="KeyFactsExtension")
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

        price_div = value.find("div", class_="bp-Homecard__SmallestUnit flex flex-grow flex-wrap align-baseline color-text-primary font-headline-xsmall")
        price = price_div.get_text(strip=True) if price_div else None

        data.append({
            "Address": address,
            "Rental Price" : price,
            "Description of the Rental Space": description,
            "Contact": contact
        })


df = pd.DataFrame(data)
# Rental_Price = df.to_csv("Rental_Price.csv", index=False)

print(df)