# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code to the container
COPY . /app/

# Expose the application on port 5000
EXPOSE 5000

# Command to run the app
CMD ["python", "app/app.py"]

