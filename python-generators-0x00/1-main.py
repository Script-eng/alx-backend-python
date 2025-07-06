#!/usr/bin/env python3

from itertools import islice
stream_users = __import__('0-stream_users').stream_users

# Iterate over the generator function and print only the first 6 rows
print("Streaming the first 6 users from the database:")
for user in islice(stream_users(), 6):
    print(user)