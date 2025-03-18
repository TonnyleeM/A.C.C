import requests
import json
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
    url = f"https://en.wikipedia.org/wiki/Culture_of_{country.replace(' ', '_')}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text  
        return None

def extract_summary(html_content):
    # Use BeautifulSoup to parse the HTML and extract the culture summary
    soup = BeautifulSoup(html_content, 'html.parser')
    summary = soup.find('div', class_='mw-parser-output')

    if summary:
        # Extract text and return it
        return summary.get_text(separator="\n", strip=True)
    else:
        return "Summary not found"

# Fetch culture summaries for all African countries
african_country_cultures = {}

for country in african_countries:
    html_content = fetch_country_culture(country)
    if html_content:
        culture_summary = extract_summary(html_content)
        african_country_cultures[country] = culture_summary
        print(f"Data extracted for {country}:")
        print(culture_summary[:200] + '...')
    else:
        african_country_cultures[country] = "Data not found"
        print(f"Data not found for {country}")

# Save the culture summaries to a JSON file in the specified format
with open('african_culture_summaries.json', 'w') as json_file:
    json.dump(african_country_cultures, json_file, indent=4)

print("Culture summaries saved to african_culture_summaries.json")