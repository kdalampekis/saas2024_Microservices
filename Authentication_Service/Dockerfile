# Use an official Python runtime as a base image
# Replace `myservice` with the actual name of the service like user-service, credit-service, etc.
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Assuming each service has its own requirements.txt
COPY Authentication_Service/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project directory
COPY Authentication_Service/ ./

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
