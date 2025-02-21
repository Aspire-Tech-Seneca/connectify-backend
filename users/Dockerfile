# Use a Python base image
FROM python:3.13.1-slim-buster 

# Set environment variables (optional, but good practice)
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE your_project.settings  # Replace your_project

# Create a working directory inside the container
WORKDIR /app

# Copy requirements file first (for caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project code
COPY . /app/

# Collect static files 
RUN python manage.py collectstatic --noinput

# Run migrations (if needed)
RUN python mongo-migrations.py/0002_populate_data.py

# Expose the port your Django app runs on (default is 8000)
EXPOSE 8000

# Start your Django development server (for development)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# For production, use a WSGI server like Gunicorn
# CMD ["gunicorn", "--bind=0.0.0.0:8000", "your_project.wsgi"]