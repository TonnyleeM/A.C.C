from flask import Flask, jsonify, request, redirect, url_for, session, render_template
from flask_cors import CORS
from flask_oauthlib.client import OAuth
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

# Links to HTML pages
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

# Login Check
def get_user(username, password):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route("/login_check", methods=["POST"])
def login_check():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = get_user(username, password)
    if user:
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401


def save_user(email, username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", 
                       (email, username, ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username or email already exists
    finally:
        conn.close()



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

@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    username = new_user.get('username')
    password = new_user.get('password')
    email = new_user.get('email')
    phone = new_user.get('phone')
    interests = new_user.get('interests')
    user_type = new_user.get('user_type')

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute(f'''
    SELECT * FROM {users_table_name} WHERE email = ?
    ''', (email,))
    
    if cursor.fetchone() is None:
        # If not exists, insert into the database
        cursor.execute(f'''
        INSERT INTO {users_table_name} (username, password, email, phone, interests, user_type)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password, email, phone, interests, user_type))
    else:
        # Update the existing record if needed
        cursor.execute(f'''
        UPDATE {users_table_name} 
        SET username = ?, password = ?, phone = ?, interests = ?, user_type = ?
        WHERE email = ?
        ''', (username, password, phone, interests, user_type, email))
    
    conn.commit()
    conn.close()
    return jsonify(new_user), 201

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