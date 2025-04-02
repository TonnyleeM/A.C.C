African Cultures Connected Project

Setup Instructions

Overview

This section provides step-by-step instructions for setting up the African Cultures Connected project on your local machine or server. Kindly follow the instructions below to ensure a smooth and seamless installation process.

Prerequisites

Python: Ensure that Python is installed on your device. You can download it from https://www.python.org/downloads/ .
SQLite: This comes bundled with Python, so you typically don't need a separate installation.
IDE: This will be used to run the program. Visual Studio Code, Git or even Powershell are ideal.
Any web browser: Chrome, Opera, Edge or other sufficient browser to interact with the application.

Installation Steps

Clone the Repository
Open your terminal or command prompt.
Navigate to the directory where you want to store the project.
Clone the repository using the command:
	git clone {SSH/HTTPS URL}:  
SSH - git@github.com:TonnyleeM/A.C.C.git,
HTTPS - https://github.com/TonnyleeM/A.C.C.git

Navigate to the Project Directory
Navigate to the project directory
cd African_Cultures_Connected

Install Required Packages

You need to install certain Python packages for the project. For ease these requirements can be found within a requirements.txt file in your project directory. It has the following content:
Flask
Flask-Cors
Flask-OAuthlib
Werkzeug
Install the required packages using pip
(pip install -r requirements.txt)

Prepare JSON Files

Ensure you have the required JSON files in your directory:
african_summaries.json: Contains summaries of countries.
african_countries_data.json: Contains data about destinations.
 Run the Python Script
Open your terminal in the project directory.
Run the main Python script to set up the database and populate it with data:

python acc_app.py

Start the Application

Access the application in your web browser at http://127.0.0.1:5000
.
You are now ready to create your account and experience the culture of your choice!
