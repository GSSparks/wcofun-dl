# Use the official Python image as the base image
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add the Mozilla signing key
RUN wget -q -O - https://mozilla.debian.net/archive.asc | apt-key add -

# Add the Mozilla repository
RUN echo "deb http://mozilla.debian.net/ $(lsb_release -cs) firefox-esr" >> /etc/apt/sources.list.d/mozilla.list

# Install geckodriver 0.34.0
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.34.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.34.0-linux64.tar.gz

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements to the container
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script to the container
COPY wcofun-dl.py wcofun-dl.py

# Specify the command to run the script
ENTRYPOINT ["python", "wcofun-dl.py"]

# Specify the volume
VOLUME ["/downloads"]

# Set the default working directory
WORKDIR /downloads
