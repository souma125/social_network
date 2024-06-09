# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install system dependencies
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential pkg-config\
    && rm -rf /var/lib/apt/lists/*


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run Django server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
