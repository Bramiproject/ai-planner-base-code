FROM python:3.11.1-slim

WORKDIR /

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8002

# Command to run the application
CMD ["python", "-u", "api/api-main.py"]
