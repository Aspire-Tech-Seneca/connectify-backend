# connectify-backend

## Create and activate virtual environment
```
cd connectify
python3 -m venv venv
source venv/bin/activate
```

## Install requirements.txt
```
pip install -r requirements.txt
```

## Create your SECRET_KEY
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the secret key into .env

## Run migration
```
python manage.py migrate
```

## Create a superuser
```
python manage.py createsuperuser
```


## Run Django webserver
```
python manage.py runserver
```
