FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MajiSafi.wsgi:application"]
