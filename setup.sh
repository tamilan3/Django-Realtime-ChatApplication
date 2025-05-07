#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting Django project setup..."

# Update package list and install Python3, pip, and virtualenv if not already installed
echo "Installing dependencies..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required Python packages
echo "Installing required Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

echo "Setup complete. You can now run the server using 'python manage.py runserver'."