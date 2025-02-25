# Connectify Backend - Django + PostgreSQL

## Development Environment Settings

### 1. Django

> **_Note:_** to install `psycopg2`, one of the most popular PostgreSQL adapters for using PostgreSQL in a Django project, the PostgreSQL development libraries (i.e., postgresql) or Python development headers that are needed to compile the C extensions in `psycopg2` is required on the host.

### 2. PostgreSQL

During development phase, run a PostgreSQL container on the host with `.env` and `init.sh` in the database directory.

## Steps to test code in this repo

### 1. Run a PostgreSQL container

Goto the database directory

```cd database```

Check if the `init.sh` file has execute permission, if not

```chmod +x init.sh```

Run docker container

```./init.sh```


### 2. Install all dependencies

Go back to the root directory

```cd ..```

Python virtual environment (some minor differences if you are using Windows)

```
python -m venv .venv 
source .venv/bin/activate
```

Install dependencies

```pip install -r requirements.txt```


### 3. Make migrations and migrate

For development purpose, the .env file is included in the repo. It includes necessary environment variables to ensure code runs smoothly

```
python manage.py makemigrations
python manage.py migrate
```

> **_Note:_** If something wrong when you run `python manage.py makemigrations`, try deleting `0001_initial.py` and run the command again.

### 4. Run server

```
python manage.py runserver
```

### 5. Test

Test URL: http://127.0.0.1:8000/users/api_name. api_name list:
```
create
login
logout
update
delete
change-password
```

> **_Note:_** Don't use two simple password when you call `change_password` API.

When successfully login, two tokens will be returned with the response: refresh token and access token.

- refresh token: test `logout`;

  In the body of the request, add:
    {
      "refresh": "<the-refresh-token>"
    }


- access token: test `update, delete, change-password`

  In the header of the request, add one more header:
  - Authorization
  - Bearer <the-access-token>
