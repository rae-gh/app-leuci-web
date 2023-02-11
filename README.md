
# AzureWebGitPlots
A demo project for deploying plot making websites to Azure

Deployed to: deployed to: http://rachel-django.azurewebsites.net

# Instructions for a tutorial on this on the wiki
https://github.com/RachelAlcraft/AzureWebGitPlots/wiki

# Other docs
https://learn.microsoft.com/en-us/training/paths/django-create-data-driven-websites/
https://www.youtube.com/watch?v=gDSp0LAs208&list=PLlrxD0HtieHjHCQ0JB_RrhbQp_9ccJztr


# Some instructions
### Activate/install virtual environment
```
python3 -m venv .venv

# Then before you activate it add in this to the bottom of the Activate file as per above (this means you can add data to the SQLite database from a script):
set DJANGO_SETTINGS_MODULE=mysite.settings

source ./.venv/bin/activate
(deactivate)
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
```
python manage.py makemigrations
python manage.py migrate
```
If you install the SQLite extension you can open the browser from the command pallette.

### Add data to database and update
Use shell command
```
python manage.py shell
```
or create a util script - see db_examples.py


### admin
superuser=admin / @Dm1n




