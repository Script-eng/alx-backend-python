#!/usr/bin/env python3
"""
Module for lazily paginating user data from a database.
"""
# Import the seed module to get access to the database connection functions
seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database.
    
    Args:
        page_size (int): The number of users to fetch.
        offset (int): The starting point from which to fetch users.
    
    Returns:
        list: A list of user dictionaries.
    """
    # Use the provided function to connect to the 'ALX_prodev' database
    connection = seed.connect_to_prodev()
    if not connection:
        print("Database connection failed.")
        return []

    cursor = connection.cursor(dictionary=True)
    
    # Safely cast page_size and offset to int to prevent SQL injection issues
    query = f"SELECT * FROM user_data LIMIT {int(page_size)} OFFSET {int(offset)}"
    cursor.execute(query)
    
    rows = cursor.fetchall()
    
    # The 'age' column is a Decimal, convert it to int for consistency
    for row in rows:
        row['age'] = int(row['age'])

    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    A generator that lazily fetches paginated data.
    It yields one page at a time, calling paginate_users only when the
    next page is requested.

    Args:
        page_size (int): The number of users per page.

    Yields:
        list: A page (list of user dictionaries).
    """
    offset = 0
    # --- This is the single required loop ---
    while True:
        # Fetch the next page of users. This is the "lazy" part.
        # This database call only happens when the loop continues.
        page = paginate_users(page_size=page_size, offset=offset)

        # If the returned page is empty, it means we have reached the end
        # of the data. We break the loop to stop the generator.
        if not page:
            break

        # Yield the fetched page and pause execution until the next one is requested
        yield page

        # Prepare the offset for the next iteration
        offset += page_size