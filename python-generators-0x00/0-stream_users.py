#!/usr/bin/env python3
"""
Module with a generator function to stream users from a MySQL database.
"""
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "ALX_prodev"

def stream_users():
    """
    A generator that connects to the user_data table and yields rows
    one by one as dictionaries.
    
    This function uses an unbuffered cursor to ensure that data is
    streamed from the server without being fully loaded into memory.
    """
    connection = None
    cursor = None
    try:
        # Establish connection to the database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        # Use an unbuffered cursor for true streaming
        cursor = connection.cursor(dictionary=True, buffered=False)
        
        query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(query)
        
        # This is the single loop that iterates over the generator cursor
        for row in cursor:
            # The row is already a dictionary thanks to `dictionary=True`
            # The 'age' field is a Decimal, convert it to a standard int
            row['age'] = int(row['age'])
            yield row

    except Error as e:
        print(f"A database error occurred: {e}")
    finally:
        # Ensure resources are closed properly
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()