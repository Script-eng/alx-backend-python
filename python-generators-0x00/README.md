Python MySQL Data Streamer
This project demonstrates how to efficiently stream data from a MySQL database row by row using a Python generator. This approach is memory-efficient, as it avoids loading the entire result set into memory, making it ideal for handling large datasets.

The project is divided into two main parts:

Seeding (seed.py, 0-main.py): A set of scripts to set up a MySQL database, create a table, and populate it with sample data from a CSV file.
Streaming (stream_data.py): A script containing a generator function that connects to the populated database and yields rows one by one.