# Use an official Python runtime as the base image
FROM python:3.10.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN python -m venv env
RUN . env/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . .

# Run the Django migrations
# RUN python manage.py migrate

# Load the fixtures into the database
# RUN python manage.py loaddata property.json

# Expose the port on which the Django application will run
# EXPOSE 8000

# Start the Django development server
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]