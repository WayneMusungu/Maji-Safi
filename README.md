# Maji-Safi
A project to offer safe drinking water

## Cloning the repository
Clone the repository using the command below :

```bash
https://github.com/WayneMusungu/Maji-Safi.git

```

Move into the directory where we have the project files :
```bash
cd Maji-Safi

```

Create your `.env` file and pass in the env variables like in the sample below, Check `.env-sample` file:
```bash
SECRET_KEY=yoursecretkeyhere
DEBUG=True # Set to False when deploying to production

#Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Add Google API
GOOGLE_API_KEY=config('GOOGLE_API_KEY')

# Paypal Configuration
PAYPAL_CLIENT_ID= config('PAYPAL_CLIENT_ID')

```

## Install Docker
The first step is to sign up for a free account on [Docker Hub](https://hub.docker.com/signup) and install Docker on your local machine by following this [installation link](https://docs.docker.com/get-docker/)

Once Docker is done installing, we can confirm the correct version is running by typing the command below in the command line shell
```bash
docker --version
```

### Building a Docker image for our application 
A Docker image is a read-only template that describes how to create a Docker container. To build an optimized docker image of our app with one command, run the command below from the root folder where `Dockerfile` is located.
```bash
docker-compose up -d --build
```

### New Database and SuperUser
Apply migrations to the application by running the command
```bash
docker-compose exec web python manage.py migrate
```

and create superuser using the command below
```bash
docker-compose exec web python manage.py createsuperuser
```

### Running tests
To run tests, use the following command:

```bash
docker-compose exec web python manage.py test
```

### View Application
> ⚠ Then, the development server will be started at http://127.0.0.1:8000/
