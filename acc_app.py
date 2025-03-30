from flask import Flask, jsonify, request, redirect, url_for, session, render_template
from flask_cors import CORS
from flask_oauthlib.client import OAuth
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
CORS(app)  # Enable CORS for all routes
oauth = OAuth(app)

# Configure the OAuth2 provider (Google in this case)
google = oauth.remote_app(
    'google',
    consumer_key='YOUR_CLIENT_ID',  # Replace with your Google Client ID
    consumer_secret='YOUR_CLIENT_SECRET',  # Replace with your Google Client Secret
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

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

# Load country data from JSON file and insert it into the database
with open('african_summaries.json', 'r') as file:
    country_data = json.load(file)

def insert_country_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for country, description in country_data.items():
        map_url = f"https://www.google.com/maps/place/{country.replace(' ', '+')}"
        
        # Check if the country already exists
        cursor.execute(f'''
        SELECT * FROM {country_table_name} WHERE country_name = ?
        ''', (country,))
        
        if cursor.fetchone() is None:
            # If not exists, insert into the database
            cursor.execute(f'''
            INSERT INTO {country_table_name} (country_name, description, map_url)
            VALUES (?, ?, ?)
            ''', (country, description, map_url))
        else:
            # Optionally, update the existing record if needed
            cursor.execute(f'''
            UPDATE {country_table_name} 
            SET description = ?, map_url = ?
            WHERE country_name = ?
            ''', (description, map_url, country))
    
    conn.commit()
    conn.close()

# Insert country data, if not already present
insert_country_data()

# Links to all HTML pages (SD)
@app.route('/', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     connection = sqlite3.connect('African_Cultures_Connected.db')
    #     cursor = connection.cursor()
    #     username = request.form['username']
    #     password = request.form['password']
    #     print(username, password)
    #     query = "SELECT username,password FROM users WHERE username= '"+username+"' AND password= '"+password+"'"
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #     if len(result) == 0:
    #         print("Login failed")
    #     else:
    #         print("Login successful")
    #         return render_template('homepage.html')

    # return google.authorize(callback=url_for('authorized', _external=True))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/operator_login', methods=['GET', 'POST'])
def operator_login():
    return render_template('operator-login.html')

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')

@app.route('/tour-booking', methods=['GET', 'POST'])
def tour_booking():
    return render_template('tour-booking.html')

@app.route('/country_profile', methods=['GET', 'POST'])
def country_profile():
    return render_template('country-profile.html')

@app.route('/tour_operator', methods=['GET', 'POST'])
def tour_operator():
    return render_template('tour-operator.html')

@app.route('/tour_booker', methods=['GET', 'POST'])
def tour_booker():
    return render_template('tour-booker.html')

@app.route('/tour_confirm', methods=['GET', 'POST'])
def tour_confirm():
    return render_template('tour-confirm.html')

@app.route('/tour_guide_search', methods=['GET', 'POST'])
def tour_guide_search():
    return render_template('tour-guide-search.html')

@app.route('/user_settings', methods=['GET', 'POST'])
def user_settings():
    return render_template('user-settings.html')

# Load user from db (SD)
@app.route("/get_user", methods=["POST"])
def get_user_api():
    # Extract the JSON data sent by JavaScript
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    # Fetch the user from the database
    conn = sqlite3.connect('African_Cultures_Connected.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Assuming the user data is returned as a tuple, convert it to a dictionary
        user_data = {
            'username': user[1],
            'userType': user[6],  # Adjust index based on your database schema
            'interests': user[5],  # Adjust accordingly if interests are stored in the database
        }
        return jsonify({'success': True, 'user': user_data})
    else:
        return jsonify({'success': False, 'message': 'User not found or incorrect password'}), 404

def get_user(username, password):
    conn = sqlite3.connect('African_Cultures_Connected.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Login Check (SD)
@app.route("/login_check", methods=["POST"])
def login_check():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user_id = data.get("user_id")

    user = get_user(username, password)
    if user:
        return jsonify({"success": True, "message": "Login successful", "user_id": user_id, "username": username, "password": password})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

# Registering a New User (SD)
@app.route('/add_user', methods=['POST'])
def add_user():
    new_user = request.get_json()
    print("Received user data:", new_user)
    username = new_user.get('username')
    password = new_user.get('password')
    email = new_user.get('email')
    phone = new_user.get('phone')
    interests = new_user.get('interests')
    user_type = new_user.get('user_type')

 
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {users_table_name} WHERE email = ?', (email,))
    
    if cursor.fetchone() is None:
        cursor.execute(f'''
        INSERT INTO {users_table_name} (username, password, email, phone, interests, user_type)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password, email, phone, interests, user_type))

    else:
        return jsonify({"success": False, "message": f"User Already Exists"}), 500
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()  
    return jsonify({"success": True, "message": "User registered successfully!", "user_id": user_id}), 201

# Registering a New Operator (SD)
@app.route('/save_operator', methods=['POST'])
def save_operator():
    new_operator = request.get_json()
    print("Received operator data:", new_operator)
    country = new_operator.get('country')
    company_name = new_operator.get('company')
    expertise = new_operator.get('expertise')
    services_offered = new_operator.get('services_offered')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if an operator with the same country and company exists
    cursor.execute('SELECT * FROM tour_operators WHERE country_id = ? AND company_name = ?', (country, company_name))

    if cursor.fetchone() is None:
        cursor.execute('''
        INSERT INTO tour_operators (country_id, company_name, expertise, services_offered)
        VALUES (?, ?, ?, ?)
        ''', (country, company_name, expertise, services_offered))
    else:
        return jsonify({"success": False, "message": "Operator with the same country and company already exists"}), 500
    
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Operator information saved successfully!"}), 201

# Removing a User (SD)
@app.route('/delete_user', methods=['POST'])
def delete_user():
    # Get the username from the request data
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({"success": False, "message": "Username is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(f'SELECT * FROM {users_table_name} WHERE username = ?', (username,))
    user = cursor.fetchone()


    if user:
        cursor.execute(f'SELECT user_id, user_type FROM {users_table_name} WHERE username = ?', (username,))
        user_id, user_type = cursor.fetchone()
        if user_type == "operator":
            cursor.execute(f'DELETE FROM {tour_operators_table_name} WHERE user_id = ?', (user_id,))
        # User exists, so delete it
        cursor.execute(f'DELETE FROM {users_table_name} WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "User deleted successfully!"}), 200
    else:
        conn.close()
        return jsonify({"success": False, "message": "User not found"}), 404


# Page to handle 404 error pages (SD)
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404 

# Page to handle other error pages (SD)
@app.errorhandler(Exception)
def handle_exception(error):
    return render_template("404.html"),

@app.route('/get_country', methods=['POST'])
def get_country_api():
    data = request.get_json()
    country_name = data.get('selectedCountry')

    if not country_name:
        return jsonify({'success': False, 'message': 'Country name not received'}), 400

    
    conn = sqlite3.connect('African_Cultures_Connected.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM country_summaries WHERE country_name = ?", (country_name,))
    country = cursor.fetchone()
    conn.close()

    if country:
        user_data = {
            'country_id': country[0],
            'country_name': country[1], 
            'description': country[2], 
            'map_url' : country[3]
        }
        return jsonify({'success': True, 'user': user_data})
    else:
        return jsonify({'success': False, 'message': 'Cuntry not found'}), 404

# Helper function to query the database
def get_destinations_by_country(country_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT destination_id, name, description FROM destinations WHERE country_id = ?", (country_id,))
    destinations = [{"destination_id": row[0], "name": row[1], "description": row[2]} for row in cursor.fetchall()]
    conn.close()
    return destinations

# Page to handle other error pages (SD)
@app.route('/get_tours', methods=['POST'])
def get_tours():
    data = request.get_json()
    country_name = data.get('country_name')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM country_summaries WHERE country_name = ?", (country_name,))
    country = cursor.fetchone()
    conn.close()
    print(country)
    if country:
        country_id = country[0]
        destinations = get_destinations_by_country(country_id)
        return jsonify(destinations)
    else:
        return jsonify({"error": "Country not found"}), 404


@app.route('/get_tour_info', methods=['POST'])
def get_tour_info():
    data = request.get_json()
    destinationName = data.get('destinationName')
    
    # Fetch country ID from country_summaries table
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM destinations WHERE name = ?", (destinationName,))
    tour_info = cursor.fetchone()
    print(tour_info)
    conn.close()

    if tour_info:
        return jsonify(tour_info)
    else:
        return jsonify({"error": "Country not found"}), 404

@app.route('/get_tour_operators', methods=['POST'])
def get_tour_operators():
    try:
        # Get the company name (destination name) from the request
        data = request.get_json()
        company_name = data.get('company_name')
        
        if not company_name:
            return jsonify({'error': 'Company name is required'}), 400
        
        # Database query to join the tables
        query = """
            SELECT u.username, u.email, u.phone, u.interests, u.user_type, 
                   t.operator_id, t.company_name, t.expertise, t.services_offered 
            FROM tour_operators t
            JOIN users u ON t.user_id = u.user_id
            JOIN destinations d ON t.country_id = d.country_id
            WHERE d.name = ?
        """
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, (company_name,))
        operators = cursor.fetchall()
        conn.close()
        
        # If no operators are found
        if not operators:
            return jsonify({'message': 'No operators found for this company'}), 404
        
        # Format the result as a list of dictionaries
        operators_list = []
        for operator in operators:
            operators_list.append({
                'operator_id': operator['operator_id'],
                'username': operator['username'],
                'email': operator['email'],
                'phone': operator['phone'],
                'interests': operator['interests'],
                'user_type': operator['user_type'],
                'company_name': operator['company_name'],
                'expertise': operator['expertise'],
                'services_offered': operator['services_offered']
            })
        
        return jsonify({'operators': operators_list}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500





@app.route('/callback')
def authorized():
    response = google.authorized_response()
    if response is None or 'access_token' not in response:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    
    # User information handling
    email = user_info.data['email']
    username = email.split('@')[0]  # Create username from email

    # Insert or update user in the database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(f'''
        INSERT INTO {users_table_name} (username, email) VALUES (?, ?)
        ON CONFLICT(email) DO UPDATE SET username = ?
    ''', (username, email, username))
    
    conn.commit()
    conn.close()

    return f'Logged in as: {email}'

@app.route('/countries', methods=['POST'])
def add_country():
    new_country = request.json
    country_name = new_country.get('country_name')
    description = new_country.get('description')

    map_url = f"https://www.google.com/maps/place/{country_name.replace(' ', '+')}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if country exists
    cursor.execute(f''' 
    SELECT * FROM {country_table_name} WHERE country_name = ?
    ''', (country_name,))
    
    if cursor.fetchone() is None:
        # If not exists, insert into the database
        cursor.execute(f'''
        INSERT INTO {country_table_name} (country_name, description, map_url)
        VALUES (?, ?, ?)
        ''', (country_name, description, map_url))
    else:
        # Update the existing record if needed
        cursor.execute(f'''
        UPDATE {country_table_name} 
        SET description = ?, map_url = ?
        WHERE country_name = ?
        ''', (description, map_url, country_name))
    
    conn.commit()
    conn.close()
    return jsonify(new_country), 201

@app.route('/destinations', methods=['POST'])
def add_destination():
    new_destination = request.json
    country_id = new_destination.get('country_id')
    name = new_destination.get('name')
    description = new_destination.get('description')
    location = new_destination.get('location')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if destination exists
    cursor.execute(f'''
    SELECT * FROM {destination_table_name} WHERE name = ? AND country_id = ?
    ''', (name, country_id))
    
    if cursor.fetchone() is None:
        # If not exists, insert into the database
        cursor.execute(f'''
        INSERT INTO {destination_table_name} (country_id, name, description, location)
        VALUES (?, ?, ?, ?)
        ''', (country_id, name, description, location))
    else:
        # Update the existing record if needed
        cursor.execute(f'''
        UPDATE {destination_table_name} 
        SET description = ?, location = ?
        WHERE name = ? AND country_id = ?
        ''', (description, location, name, country_id))
    
    conn.commit()
    conn.close()
    return jsonify(new_destination), 201

@app.route('/tour_operators', methods=['POST'])
def add_tour_operator():
    new_operator = request.json
    user_id = new_operator.get('user_id')
    country_id = new_operator.get('country_id')
    company_name = new_operator.get('company_name')
    expertise = new_operator.get('expertise')
    services_offered = new_operator.get('services_offered')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if tour operator exists
    cursor.execute(f'''
    SELECT * FROM {tour_operators_table_name} WHERE company_name = ? AND user_id = ?
    ''', (company_name, user_id))
    
    if cursor.fetchone() is None:
        # If not exists, insert into the database
        cursor.execute(f'''
        INSERT INTO {tour_operators_table_name} (user_id, country_id, company_name, expertise, services_offered)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, country_id, company_name, expertise, services_offered))
    else:
        # Update the existing record if needed
        cursor.execute(f'''
        UPDATE {tour_operators_table_name} 
        SET country_id = ?, expertise = ?, services_offered = ?
        WHERE company_name = ? AND user_id = ?
        ''', (country_id, expertise, services_offered, company_name, user_id))
    
    conn.commit()
    conn.close()
    return jsonify(new_operator), 201

@app.route('/tours', methods=['POST'])
def add_tour():
    new_tour = request.json
    operator_id = new_tour.get('operator_id')
    destination_id = new_tour.get('destination_id')
    tour_name = new_tour.get('tour_name')
    description = new_tour.get('description')
    price = new_tour.get('price')
    duration = new_tour.get('duration')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if tour exists
    cursor.execute(f'''
    SELECT * FROM {tours_table_name} WHERE tour_name = ? AND operator_id = ?
    ''', (tour_name, operator_id))
    
    if cursor.fetchone() is None:
        # If not exists, insert into the database
        cursor.execute(f'''
        INSERT INTO {tours_table_name} (operator_id, destination_id, tour_name, description, price, duration)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (operator_id, destination_id, tour_name, description, price, duration))
    else:
        # Update the existing record if needed
        cursor.execute(f'''
        UPDATE {tours_table_name} 
        SET destination_id = ?, description = ?, price = ?, duration = ?
        WHERE tour_name = ? AND operator_id = ?
        ''', (destination_id, description, price, duration, tour_name, operator_id))
    
    conn.commit()
    conn.close()
    return jsonify(new_tour), 201

@app.route('/bookings', methods=['POST'])
def add_booking():
    new_booking = request.json
    user_id = new_booking.get('user_id')
    tour_id = new_booking.get('tour_id')
    booking_date = new_booking.get('booking_date')
    status = new_booking.get('status')
    total_cost = new_booking.get('total_cost')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if booking exists
    cursor.execute(f'''
    SELECT * FROM {bookings_table_name} WHERE user_id = ? AND tour_id = ? AND booking_date = ?
    ''', (user_id, tour_id, booking_date))
    
    if cursor.fetchone() is None:
        # If not exists, insert into the database
        cursor.execute(f'''
        INSERT INTO {bookings_table_name} (user_id, tour_id, booking_date, status, total_cost)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, tour_id, booking_date, status, total_cost))
    else:
        # Update the existing record if needed
        cursor.execute(f'''
        UPDATE {bookings_table_name} 
        SET status = ?, total_cost = ?
        WHERE user_id = ? AND tour_id = ? AND booking_date = ?
        ''', (status, total_cost, user_id, tour_id, booking_date))
    
    conn.commit()
    conn.close()
    return jsonify(new_booking), 201

@google.tokengetter
def get_google_oauth2_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run(debug=True)