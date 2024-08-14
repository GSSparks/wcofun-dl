# Use the official Python image as the base image
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install geckodriver 0.34.0
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.35.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.35.0-linux64.tar.gz

# Copy the requirements to the container
COPY ./requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the script to the container
COPY ./wcofun-dl.py /opt/wcofun-dl.py

# Specify the command to run the script
ENTRYPOINT ["python", "/opt/wcofun-dl.py"]

# Specify the volume
VOLUME ["/downloads"]

# Set the default working directory
WORKDIR /downloads
