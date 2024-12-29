
# Leuci-Web
An application for browsing electron density maps online

This uses python libraries available on PyPi

# Some instructions
### Activate/install virtual environment
```
python3 -m venv .venv-leuci
source .venv-leuci/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade

```

### Run the server locally using
```
python manage.py runserver
uvicorn project.asgi:application
uvicorn project.asgi:application --reload

or
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
python manage.py runserver_plus


```
http://127.0.0.1:8000/

http://127.0.0.1:8000/admin/

### Databases
If necessary run the migrations on first clone
```
python manage.py makemigrations
python manage.py migrate
```
If you want to get the static files together for debug False locally:
```
python manage.py collectstatic
```
### Deploying to azure from vscode
There is a free deployment at [maptial@azure](https://maptial.azurewebsites.net/).  
This is not satisfactory but it is better than nothing.  
The free hosting for python apps is very bad and most things areimpossible to do.  
This applicaiton os pretyy intensive for both data size, data download, and calculations.  





