#!/usr/bin/env python3
"""
Module to fetch and process user data in batches.
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

def stream_users_in_batches(batch_size=50):
    """
    A generator that connects to the user_data table and yields rows
    in batches of a specified size.

    Args:
        batch_size (int): The number of rows to fetch in each batch.

    Yields:
        list: A list of user dictionaries representing a batch.
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
        # Use a dictionary cursor for easy data handling and unbuffered for streaming
        cursor = connection.cursor(dictionary=True, buffered=False)
        
        query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(query)

        batch = []
        # --- LOOP 1: Iterates through every row from the database ---
        for row in cursor:
            row['age'] = int(row['age']) # Convert Decimal to int
            batch.append(row)
            if len(batch) >= batch_size:
                yield batch
                batch = [] # Reset the batch

        # Yield any remaining users in the last, possibly smaller, batch
        if batch:
            yield batch

    except Error as e:
        print(f"A database error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size=50):
    """
    Processes batches of users to filter for users over the age of 25
    and prints their information.

    Args:
        batch_size (int): The size of batches to process.
    """
    # --- LOOP 2: Iterates through each batch yielded by the generator ---
    for batch in stream_users_in_batches(batch_size=batch_size):
        # --- LOOP 3: Iterates through each user within a batch ---
        for user in batch:
            if user['age'] > 25:
                # The extra print() adds the blank line seen in the example output
                print(user)
                print() 