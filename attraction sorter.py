import json

# Load the original JSON data from the file
with open('africa_attractions_data.json', 'r') as json_file:
    locations = json.load(json_file)

# Group locations by country
grouped_locations = {}
for location in locations:
    country = location["city"]
    if country not in grouped_locations:
        grouped_locations[country] = []
    grouped_locations[country].append(location)

# Sort each country's locations by name
for country in grouped_locations:
    grouped_locations[country] = sorted(grouped_locations[country], key=lambda x: x['name'])

# Save the grouped and sorted data to a new JSON file
with open('grouped_sorted_africa_attractions_data.json', 'w') as grouped_json_file:
    json.dump(grouped_locations, grouped_json_file, indent=4)

print("Grouped and sorted data saved to grouped_sorted_africa_attractions_data.json")