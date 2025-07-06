#!/usr/bin/env python3
import os
import csv
import uuid
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Database Configuration ---
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "ALX_prodev"

def connect_db():
    """Connects to the MySQL database server."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created or already exists.")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print(f"Error while connecting to '{DB_NAME}': {e}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3, 0) NOT NULL,
        UNIQUE(email)
    ) ENGINE=InnoDB;
    """
    try:
        cursor.execute(create_table_query)
        print("Table 'user_data' created or already exists.")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

def insert_data(connection, csv_filename):
    """
    Reads data from a CSV file and inserts it into the user_data table.
    It ignores rows with duplicate emails to prevent errors on re-runs.
    """
    # Read and prepare data from CSV
    data_to_insert = []
    try:
        with open(csv_filename, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row
            for row in reader:
                # Each row is (name, email, age)
                # We add a UUID for the user_id
                data_to_insert.append((str(uuid.uuid4()), row[0], row[1], int(row[2])))
    except FileNotFoundError:
        print(f"Error: The file '{csv_filename}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    if not data_to_insert:
        print("No data to insert.")
        return

    # Use INSERT IGNORE to skip inserting rows that would cause a duplicate entry
    # for the 'email' unique key.
    insert_query = """
    INSERT IGNORE INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    cursor = connection.cursor()
    try:
        cursor.executemany(insert_query, data_to_insert)
        connection.commit()
        print(f"{cursor.rowcount} new rows were inserted into 'user_data'.")
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        cursor.close()