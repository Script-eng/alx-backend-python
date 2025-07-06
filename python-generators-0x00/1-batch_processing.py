#!/usr/bin/env python3
"""
Module to fetch and process user data in batches.
This script contains no 'return' statements.
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
    A generator that yields user data in batches.
    It exclusively uses 'yield' to produce values and does not use 'return'.
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
        cursor = connection.cursor(dictionary=True, buffered=False)
        
        query = "SELECT user_id, name, email, age FROM user_data"
        cursor.execute(query)

        batch = []
        # Loop 1: Iterates through the database cursor
        for row in cursor:
            row['age'] = int(row['age'])
            batch.append(row)
            if len(batch) >= batch_size:
                yield batch  # Produces a batch
                batch = []

        # Yield the final, possibly smaller, batch after the loop.
        # The function ends here, and the generator naturally stops.
        if batch:
            yield batch

    except Error as e:
        print(f"A database error occurred: {e}")
    finally:
        # The finally block ensures resources are closed, but it does not
        # contain a 'return' statement.
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size=50):
    """
    Processes batches from the generator. This is a standard function,
    not a generator, and it completes its task without needing to 'return' a value.
    """
    # Loop 2: Iterates through the batches from the generator
    for batch in stream_users_in_batches(batch_size=batch_size):
        # Loop 3: Iterates through users in a single batch
        for user in batch:
            if user['age'] > 25:
                # Processes data by printing. No value is returned.
                print(user)
                print()
    # The function implicitly ends here after the loop is exhausted.