# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for PostgreSQL and psycopg
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8002

# Command to run the application
CMD ["python", "api/api-main.py"]

# Command to run the application
# CMD ["uvicorn", "main.prod:APP", "--host", "0.0.0.0", "--port", "5554", "--workers", "32"]