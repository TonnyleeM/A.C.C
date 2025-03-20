import http.client
import json
import urllib.parse

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

# Your API key
api_key = "YOUR_API_KEY"

# Categories to search for
categories = [
    "accommodation", "activity", "entertainment", "entertainment.culture",
    "entertainment.culture.arts_centre", "entertainment.zoo", "leisure",
    "natural", "national_park", "tourism", "tourism.attraction",
    "tourism.sights", "tourism.sights.memorial"
]

# Store results
results = {}

# Search for each category in each country
for country in african_countries:
    print(f"Fetching places for: {country}")
    
    # URL encode the country name
    encoded_country = urllib.parse.quote(country)
    
    # Construct the API request URL using multiple categories
    category_query = ','.join(categories)
    url = (
        f"https://api.geoapify.com/v2/places?categories={category_query}"
        f"&filter=name:{encoded_country}&limit=20&apiKey={api_key}"
    )
    
    # Make the request
    conn = http.client.HTTPSConnection("api.geoapify.com")
    conn.request("GET", url)
    
    res = conn.getresponse()
    data = res.read()
    
    # Decode and parse the JSON data
    response_data = json.loads(data.decode("utf-8"))
    
    # Store results
    results[country] = response_data.get('features', [])
    
    conn.close()

# Save results to a JSON file
with open('african_countries_data.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)

print("African countries data has been successfully saved to african_countries_data.json.")