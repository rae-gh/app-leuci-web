
# Leuci-Web
An application for browsing electron density maps online

This uses python libraries available on PyPi

# Some instructions
### Activate/install virtual environment
```
python3 -m venv .venv
source ./.venv/bin/activate
```
### Install the requirements
```
pip install -r requirements.txt
```
### Run the server locally using
```
python manage.py runserver
uvicorn project.asgi:application

```
http://127.0.0.1:8000/

http://127.0.0.1:8000/admin/

### Databases
If necessary run the migrations on first clone
```
python manage.py makemigrations
python manage.py migrate
```



