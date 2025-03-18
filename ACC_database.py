from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database and table names
db_name = 'African_Cultures_Connected.db'
country_table_name = 'country_summaries'
destination_table_name = 'destinations'
tour_operators_table_name = 'tour_operators'
users_table_name = 'users'
tours_table_name = 'tours'
bookings_table_name = 'bookings'

def get_db_connection():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {country_table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country_name TEXT,
        description TEXT,
        map_url TEXT
    )
    ''')

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

    conn.commit()
    conn.close()

# Call the function to create tables
create_tables()

# Load country data from JSON file and insert it into the database
with open('african_summaries.json', 'r') as file:
    country_data = json.load(file)

def insert_country_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for country, description in country_data.items():
        map_url = f"https://www.google.com/maps/place/{country.replace(' ', '+')}"
        cursor.execute(f'''
        INSERT INTO {country_table_name} (country_name, description, map_url)
        VALUES (?, ?, ?)
        ''', (country, description, map_url))
    
    conn.commit()
    conn.close()

# Insert country data, if not already present
insert_country_data()

# API Endpoints
@app.route('/countries', methods=['GET'])
def get_countries():
    conn = get_db_connection()
    countries = conn.execute('SELECT * FROM country_summaries').fetchall()
    conn.close()
    return jsonify([dict(row) for row in countries])

@app.route('/countries', methods=['POST'])
def add_country():
    new_country = request.json
    country_name = new_country.get('country_name')
    description = new_country.get('description')

    map_url = f"https://www.google.com/maps/place/{country_name.replace(' ', '+')}"
    
    conn = get_db_connection()
    conn.execute(f'''
    INSERT INTO {country_table_name} (country_name, description, map_url)
    VALUES (?, ?, ?)
    ''', (country_name, description, map_url))
    conn.commit()
    conn.close()
    return jsonify(new_country), 201

# Add similar endpoints for other tables (Destinations, Tour Operators, Users, Tours, Bookings)

if __name__ == '__main__':
    app.run(debug=True)