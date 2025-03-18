import json
import requests
from bs4 import BeautifulSoup

# List of African countries
african_countries = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
    "Congo, Republic of the", "Congo, Democratic Republic of the", "Djibouti",
    "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon",
    "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Kenya",
    "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania",
    "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria",
    "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone",
    "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo",
    "Tunisia", "Uganda", "Zambia", "Zimbabwe"
]

def fetch_country_culture(country):
    # Format the URL for the specified country
    url = f"https://en.wikipedia.org/wiki/Tourism_in_{country.replace(' ', '_')}"
    print(f"Fetching data from: {url}")  # Debugging line
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Example extraction: Get the first paragraph for culture description
        description = soup.find('p').text.strip() if soup.find('p') else "No description available"
        
        return {
            "country": country,
            "description": description,
            "url": url
        }
    else:
        print(f"Failed to retrieve data for {country}: {response.status_code}")
        return {
            "country": country,
            "description": "No data available",
            "url": url
        }

# Dictionary to hold results
results = {}

# Iterate through each country and fetch data
for country in african_countries:
    results[country] = fetch_country_culture(country)

# Save results to a JSON file
with open('african_countries_data.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)

print("African countries data has been successfully saved to african_countries_data.json.")