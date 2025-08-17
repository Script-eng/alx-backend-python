
# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Ensures Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy the dependencies file and install them
# Copy requirements.txt first to leverage Docker's layer caching.
# The layer will only be rebuilt if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code into the container
COPY . .

# Step 6: Expose the port the app runs on
# This is documentation for which port to map from the host.
EXPOSE 8000

# Step 7: Define the command to run your application
# Use 0.0.0.0 to make the server accessible from outside the container.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]