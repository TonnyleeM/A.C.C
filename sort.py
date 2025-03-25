import json

# Load data from the JSON file
with open('grouped_sorted_africa_attractions_data.json', 'r') as file:
    data = json.load(file)

# Extracting country names, destination names, and descriptions
extracted_data = []

for country, destinations in data.items():
    for destination in destinations:
        country_name = country
        destination_name = destination['name']
        description = destination['description']
        
        extracted_data.append({
            "country": country_name,
            "destination": destination_name,
            "description": description
        })

# Save extracted data to a new JSON file
with open('extracted_attractions_data.json', 'w') as outfile:
    json.dump(extracted_data, outfile, indent=4)

print("Data has been successfully extracted and saved to 'extracted_attractions_data.json'.")