#!/usr/bin/env python3
"""
A memory-efficient script to calculate the average age of users
by streaming data from a database using a generator.
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

def stream_user_ages():
    """
    A generator that connects to the database and yields user ages one by one.
    This is memory-efficient as it does not load all ages at once.

    Yields:
        int: The age of a user.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        # Use an unbuffered cursor to stream results from the server
        cursor = connection.cursor(buffered=False)
        
        # We only need the 'age' column, which is more efficient
        query = "SELECT age FROM user_data"
        cursor.execute(query)

        # --- LOOP 1: Iterates over the database cursor ---
        for row in cursor:
            # The row is a tuple, e.g., (Decimal('35'),). Get the first item.
            yield int(row[0])

    except Error as e:
        print(f"A database error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def calculate_average_age():
    """
    Calculates the average age of all users by consuming the
    stream_user_ages generator, without loading all data into memory.
    """
    total_age = 0
    user_count = 0

    # --- LOOP 2: Iterates over the ages yielded by the generator ---
    for age in stream_user_ages():
        total_age += age
        user_count += 1

    # Avoid division by zero if the database is empty
    if user_count > 0:
        average_age = total_age / user_count
        # Print the result formatted to two decimal places
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found in the database.")


if __name__ == "__main__":
    calculate_average_age()