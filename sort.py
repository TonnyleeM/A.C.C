import json

# Load data from the JSON file
with open('grouped_sorted_africa_attractions_data.json', 'r') as file:
    data = json.load(file)

# Prepare the extracted data in the desired format
extracted_data = {}

for country, destinations in data.items():
    extracted_data[country] = []
    for destination in destinations:
        # Prepare the destination entry with only name and description
        destination_entry = {
            "name": destination['name'],
            "description": destination['description']
        }
        extracted_data[country].append(destination_entry)

# Save extracted data to a new JSON file
with open('extracted_attractions_data.json', 'w') as outfile:
    json.dump(extracted_data, outfile, indent=4)

print("Data has been successfully extracted and saved to 'extracted_attractions_data.json'.")