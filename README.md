# Maji-Safi
A project to offer safe drinking water

### Cloning the repository

Clone the repository using the command below :

```bash
https://github.com/WayneMusungu/Maji-Safi.git

```

Move into the directory where we have the project files :
```bash
cd Maji-Safi

```

Create a virtual environment :
```bash
# Create our virtual environment
python -m venv venv

```

--> Activate the virtual environment : <br><br>
windows
```bash
venv\scripts\activate

```
linux
```bash
source venv/bin/activate

```

--> Install the requirements :
```bash
pip install -r requirements.txt

```

--> Migrate Database
```bash
python manage.py migrate

```

--> Create Super User
```bash
python manage.py createsuperuser

```

### Running the App

--> To run the App, we use :
```bash
python manage.py runserver

```

> ⚠ Then, the development server will be started at http://127.0.0.1:8000/
