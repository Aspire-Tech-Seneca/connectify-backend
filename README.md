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

## MongoDB is the choice
User accounts (username and email) cannot be duplicated.

## Redis may be added for fast real-time caching (optional)

## MongoEngine + Django
MongoEngine has been choosen for:
- Object-Document Mapper (ODM)
- More abstract and structured
- Easier data modeling with Python classes
- Indexes can be defined in models



# Security Considerations

## Lift CORS restrictions

1. This configuration has security issues and cannot be used in production environment

2. Install `django-cors-headers` (in the `requirements.txt`)

3. Add corsheaders to INSTALLED_APPS.

4. Add CorsMiddleware to MIDDLEWARE.

5. Allow all origins in development with CORS_ALLOW_ALL_ORIGINS = True