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


# Database
At this first stage of development, Django's default database engine sqlite3 has been used for the convenience. The MongoDB will replace sqlite3 later, and documents will be used to store users' data for their flexibilities.


# Security Considerations

## Lift CORS restrictions

1. This configuration has security issues and cannot be used in production environment

2. Install `django-cors-headers` (in the `requirements.txt`)

3. Add corsheaders to INSTALLED_APPS.

4. Add CorsMiddleware to MIDDLEWARE.

5. Allow all origins in development with CORS_ALLOW_ALL_ORIGINS = True