# Use the official Python base image
FROM python:3.11-alpine


# Create a non-root user and group
RUN addgroup -S celerygroup && adduser -S celeryuser -G celerygroup

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set permissions for the non-root user
RUN chown -R celeryuser:celerygroup /app

# Switch to the non-root user
USER celeryuser

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port number
EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]