import os
import urllib.parse
import mysql.connector
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database Configuration for Hostinger MySQL
DB_USER = "u644527998_lakender"  # Your database username
DB_PASSWORD = urllib.parse.quote_plus("tyagi_Luckyg2025")  # Encode special characters in the password
DB_HOST = "srv1836.hstgr.io"  # MySQL host
DB_NAME = "u644527998_Lumenox"  # Database name

# Function to establish database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Database connection error: {e}")
        return None

# Function to initialize the database (create ContactData table if not exists)
def init_db():
    conn = get_db_connection()
    if conn is None:
        print("❌ Could not connect to database.")
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ContactData (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                subject VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✅ Database initialized successfully.")
    except mysql.connector.Error as e:
        print(f"❌ Error initializing database: {e}")
    finally:
        cursor.close()
        conn.close()

def save_contact_form(name, email, subject, message):
    try:
        # Database Configuration
        connection = mysql.connector.connect(
            host="srv1836.hstgr.io",
            user="u644527998_lakender",
            password="tyagi_Luckyg2025",
            database="u644527998_Lumenox"
        )
        
        cursor = connection.cursor()  # ✅ Ensure cursor is initialized inside the try block

        # SQL Query
        query = "INSERT INTO ContactData (name, email, subject, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, subject, message))
        
        connection.commit()  # ✅ Commit the transaction
        return {"success": True, "message": "Data saved successfully!"}

    except mysql.connector.Error as err:
        logging.error(f"Error processing quote form: {err}")
        return {"success": False, "error": str(err)}

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()  # ✅ Close cursor safely
        if 'connection' in locals() and connection.is_connected():
            connection.close()  # ✅ Ensure connection is closed

