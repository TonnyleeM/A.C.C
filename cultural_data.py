import json
import sqlite3

# Load the JSON data
with open('african_culture_summaries.json', 'r') as file:
    data = json.load(file)

# Connect to SQLite database (or create it)
conn = sqlite3.connect('african_culture.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS cultures (
    country TEXT PRIMARY KEY,
    description TEXT
)
''')

# Insert data into the table
for country, description in data.items():
    cursor.execute('''
    INSERT INTO cultures (country, description) VALUES (?, ?)
    ''', (country, description))

# Commit and close the connection
conn.commit()
conn.close()