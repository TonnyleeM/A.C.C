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
    country_name TEXT,
    description TEXT,
    map_url TEXT
)
''')

# Create the destinations table if it doesn't exist
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {destination_table_name} (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER,
    name CHAR,
    description TEXT,
    location POINT,
    FOREIGN KEY (country_id) REFERENCES {country_table_name}(id)
)
''')

# Create the tour operators table if it doesn't exist
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {tour_operators_table_name} (
    operator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    country_id INTEGER,
    company_name CHAR,
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
    username CHAR,
    password CHAR,
    email CHAR,
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
    tour_name CHAR,
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
    INSERT INTO {country_table_name} (country_name, description, map_url)
    VALUES (?, ?, ?)
    ''', (country, description, map_url))

# Commit the changes for country summaries
conn.commit()

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully inserted into the country summaries table.")
print("All additional tables have been created empty.")