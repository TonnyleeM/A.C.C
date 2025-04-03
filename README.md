# African Cultures Connected Project

## What is ACC About?
African Cultures Connected is a platform that connects global tourists with local African tour operators. The project aims to preserve indigenous cultural heritage while creating sustainable economic opportunities for local communities. ACC serves as both a booking system and a cultural preservation tool, allowing visitors to experience authentic African traditions while ensuring revenue stays within local economies.

## Setup Instructions

### Prerequisites
- **Python**: Ensure that Python is installed on your device. You can download it from https://www.python.org/downloads/
- **SQLite**: This comes bundled with Python, so you typically don't need a separate installation.
- **IDE**: This will be used to run the program. Visual Studio Code, Git or even Powershell are ideal.
- **Any web browser**: Chrome, Opera, Edge or other sufficient browser to interact with the application.

### Installation Steps

1. **Clone the Repository**
   Open your terminal or command prompt.
   Navigate to the directory where you want to store the project.
   Clone the repository using the command:
   git clone https://github.com/TonnyleeM/A.C.C.git
   or SSH:
   git clone git@github.com/A.C.C.git
   
   2. **Navigate to the Project Directory**
  
   cd African_Cultures_Connected
3. **Install Required Packages**
You need to install certain Python packages for the project. For ease these requirements can be found within a requirements.txt file in your project directory. It has the following content:
- Flask
- Flask-Cors
- Flask-OAuthlib
- Werkzeug

Install the required packages using pip:
pip install -r requirements.txt

4. **Prepare JSON Files**
Ensure you have the required JSON files in your directory:
- african_summaries.json: Contains summaries of countries.
- african_countries_data.json: Contains data about destinations.

5. **Run the Python Script**
Open your terminal in the project directory.
Run the main Python script to set up the database and populate it with data:
python acc_app.py

6. **Start the Application**
Access the application in your web browser at http://127.0.0.1:5000

You are now ready to create your account and experience the culture of your choice!
