import json
import sqlite3

# Define the database and table name
db_name = 'african_countries.db'
table_name = 'country_summaries'

# Create a connection to the SQLite database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT,
    description TEXT,
    map_url TEXT
)
''')

# Read data from the JSON file
with open('african_summaries.json', 'r') as file:
    data = json.load(file)

# Prepare the data for insertion
for country, description in data.items():
    map_url = f"https://www.google.com/maps/place/{country.replace(' ', '+')}"
    cursor.execute(f'''
    INSERT INTO {table_name} (country_name, description, map_url)
    VALUES (?, ?, ?)
    ''', (country, description, map_url))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully inserted into the database.")