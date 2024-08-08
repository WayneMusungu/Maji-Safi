# Use the official Python base image
FROM python:3.10.4-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .