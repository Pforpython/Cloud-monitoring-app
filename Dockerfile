#Dockerfile from Youtube
# FROM python:3.13-slim-bullseye

# WORKDIR /app

# COPY requirements.txt .

# RUN pip3 install --no-cache-dir -r requirements.txt

# COPY . .

# ENV FLASK_RUN_HOST=0.0.0.0

# EXPOSE 5000

# CMD ["flask", "run"]


#Dockerfile built by Claude.ai
# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    # rm -rf /var/lib/apt/lists/* \
    pip3 install --no-cache-dir -r requirements.txt
    
# Copy the rest of the application
COPY . .

# Create templates directory and copy HTML template
# RUN mkdir -p templates

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python3", "app.py"]