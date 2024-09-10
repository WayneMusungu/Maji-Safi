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
SECRET_KEY = env('SECRET_KEY', default="secret_key")
DEBUG=True # Set to False when deploying to production

#Email Configuration
EMAIL_BACKEND=your_default_email_backend
EMAIL_HOST=your_default_email_host
EMAIL_PORT=587)  # Example default port
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_default_email_user
EMAIL_HOST_PASSWORD=your_default_email_password
DEFAULT_FROM_EMAIL=your_default_from_email

# Paypal Configuration
PAYPAL_CLIENT_ID=your_pay_pal_client_id

# Google Configuration
GOOGLE_API_KEY=your_default_google_api_key


```

## Set Up Host Gmail Account
- Go to [Security](https://myaccount.google.com/security)

- Scroll till you find **Signing in to Google**
    
    - In that section, you will see the "App Passwords" option as shown in the below image.

    ![Password](images/app_pwd.png)

    - When you click on **App Passwords**, you will be asked to enter your Gmail account password. Enter it and the page would open:

    - Follow the below steps as shown in the image to setup your app password.

    ![SetupAppPassword](images/setup_app_pwd.jpg)

- Only if you follow the above steps, then you can send mail from your Gmail account using your django code. 


## Install Docker
The first step is to sign up for a free account on [Docker Hub](https://hub.docker.com/signup) and install Docker on your local machine by following this [installation link](https://docs.docker.com/get-docker/)

Once Docker is done installing, we can confirm the correct version is running by typing the command below in the command line shell
```bash
docker --version
```

### Building a Docker image for our application 
A Docker image is a read-only template that describes how to create a Docker container. To build an optimized docker image of our app with one command, run the command below from the root folder where `Dockerfile` is located.
```bash
docker compose build
docker compose up -d
```


### SuperUser Creation
Create superuser using the command below
```bash
docker exec -it my-app-container python manage.py createsuperuser
```

### View Application
> ⚠ Then, the development server will be started at http://127.0.0.1:8000/
