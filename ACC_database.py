import json
import sqlite3

# Define the database and table names
db_name = 'African_Cultures_Connected.db'
country_table_name = 'country_summaries'
destination_table_name = 'destinations'
tour_operators_table_name = 'tour_operators'
users_table_name = 'users'
tours_table_name = 'tours'
bookings_table_name = 'bookings'

# Create a connection to the SQLite database
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create the country summaries table if it doesn't exist
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {country_table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT UNIQUE,
    description TEXT,
    map_url TEXT
)
''')

# Create the destinations table if it doesn't exist
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {destination_table_name} (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER,
    name CHAR UNIQUE,
    description TEXT,
    location TEXT,  -- Changed from POINT to TEXT for iframe link
    FOREIGN KEY (country_id) REFERENCES {country_table_name}(id)
)
''')

# Create the tour operators table if it doesn't exist
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {tour_operators_table_name} (
    operator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    country_id INTEGER,
    company_name CHAR UNIQUE,
    expertise TEXT,
    services_offered TEXT,
    FOREIGN KEY (user_id) REFERENCES {users_table_name}(user_id),
    FOREIGN KEY (country_id) REFERENCES {country_table_name}(id)
)
''')

# Create the users table if it doesn't exist
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {users_table_name} (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username CHAR UNIQUE,
    password CHAR,
    email CHAR UNIQUE,
    phone CHAR,
    interests TEXT,
    user_type CHAR CHECK(user_type IN ('tourist', 'operator'))
)
''')

# Create the tours table if it doesn't exist
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {tours_table_name} (
    tour_id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id INTEGER,
    destination_id INTEGER,
    tour_name CHAR UNIQUE,
    description TEXT,
    price DECIMAL,
    duration CHAR,
    FOREIGN KEY (operator_id) REFERENCES {tour_operators_table_name}(operator_id),
    FOREIGN KEY (destination_id) REFERENCES {destination_table_name}(destination_id)
)
''')

# Create the bookings table if it doesn't exist
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {bookings_table_name} (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    tour_id INTEGER,
    booking_date DATE,
    status CHAR CHECK(status IN ('pending', 'confirmed', 'cancelled')),
    total_cost DECIMAL,
    FOREIGN KEY (user_id) REFERENCES {users_table_name}(user_id),
    FOREIGN KEY (tour_id) REFERENCES {tours_table_name}(tour_id)
)
''')

# Read data from the country summaries JSON file
with open('african_summaries.json', 'r') as file:
    country_data = json.load(file)

# Prepare and insert data into the country summaries table
for country, description in country_data.items():
    map_url = f"https://www.google.com/maps/place/{country.replace(' ', '+')}"
    cursor.execute(f'''
    INSERT OR IGNORE INTO {country_table_name} (country_name, description, map_url)
    VALUES (?, ?, ?)
    ''', (country, description, map_url))

# Commit the changes for country summaries
conn.commit()

# Read data from the grouped_sorted_africa_attractions_data.json file
with open('african_countries_data.json', 'r') as file:
    grouped_data = json.load(file)

# Prepare and insert data into the destinations table
for country, destinations in grouped_data.items():
    # Get the country_id for the current country
    cursor.execute(f'''
    SELECT id FROM {country_table_name} WHERE country_name = ?
    ''', (country,))
    country_id = cursor.fetchone()

    if country_id:
        country_id = country_id[0]
        for destination in destinations:
            # Extract the description and iframe link
            description = destination.get('description', '')
            iframe_link = destination.get('iframe_link', '')

            cursor.execute(f'''
            INSERT OR IGNORE INTO {destination_table_name} (country_id, name, description, location)
            VALUES (?, ?, ?, ?)
            ''', (country_id, destination['name'], description, iframe_link))  # Use iframe_link for location

# Commit the changes for destinations
conn.commit()

# Close the connection
conn.close()

print("Data has been successfully inserted into the country summaries and destinations tables.")
print("All additional tables have been created empty.")