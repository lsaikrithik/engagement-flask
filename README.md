# Engagement Database Flask App

## Overview

This repository contains a Flask application for managing an engagement database with a PostgreSQL backend. Follow the steps below to set up and run the application on your local machine.

## Getting Started

### 1. Clone the Repository
To set up this project locally, first clone the repository from GitHub and navigate to the project folder:

1. **Open your terminal** (Command Prompt, Git Bash, or any terminal emulator of your choice).
   
2. **Run the following command** to clone the repository:
   ```bash
   git clone https://github.com/lsaikrithik/engagement-flask.git
   cd engagement-flask
   ```

### 2. Install PostgreSQL 13
Download and install PostgreSQL 13 from the official PostgreSQL Downloads. During installation, remember the username and password you set for the database superuser (default is usually postgres).

### 3. Connect to the PostgreSQL Server
After installation, connect to the PostgreSQL server. Use either the command line or pgAdmin:

#### Using Command Line
Open your terminal or command prompt.
Connect to PostgreSQL by running:

 ```bash
psql -U postgres
```
Replace postgres with your username if different. Enter your password when prompted.

#### Using pgAdmin
1. Open pgAdmin and log in.
2. In the left panel, right-click on Servers and select Connect Server. Enter your server details and save.

### 4. Restore the Database
If you have a backup file (e.g., `engagement.sql` or `engagement.backup`), follow these steps to restore it:

#### Using Command Line
Navigate to the folder containing your backup file.
Run:
 ```bash
psql -U postgres -d your_database_name -f backup_file.sql
```
Replace your_database_name and backup_file.sql accordingly.

#### Using pgAdmin
Right-click on the target database in pgAdmin and select Restore.
Choose your backup file, adjust any settings as needed, and click Restore.

### 5. Configure Database Credentials
In the config.py and db.py files, replace placeholders with your PostgreSQL username and password.

db.py Example
 ```bash
import psycopg2

conn = psycopg2.connect(database='engagement', host='localhost', user='username', password='password', port='5432')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS student1(id serial PRIMARY KEY, name varchar(50));''')
cur.execute('''INSERT INTO student1(id, name) VALUES (101, 'aaa');''')
conn.commit()
cur.close()
conn.close()
```

config.py Example
 ```bash
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://username:password@localhost:5432/engagement'  # Replace with your details
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```
    
### 6. Install Dependencies
Ensure you have all required Python packages installed. Create a requirements.txt file with the following contents:

 ```bash
Flask
Flask-SQLAlchemy
psycopg2-binary
SQLAlchemy
```
Then, run:

 ```bash
pip install -r requirements.txt
```

### 7. Run the Application
Start the Flask application:
 ```bash
python app.py
```

## Access the Application
Open your web browser and navigate to http://127.0.0.1:5000/ in your browser to access the app.
