# Docker Compose

0. Replace the <azure_blob_connection_string> in the `.env` file with the connection string of the Azure storage account.

1. Build Django web application image

In the root directory, run
```
 docker build -t connectify-backend-web .
```

2. Start both Django & PostgreSQL containers using Docker Compose

Still in the root directory, run

```
docker-compose up -d --build
```

3. Check running containers

```
docker ps -a
```

4. Apply migrations (optional)

```
docker exec -it <django_app_container_id> python manage.py migrate
```

5. Stop containers

Stop the containers

```
docker-compose down
docker-compose down -v
```


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

> **_Note:_** Please use connection variables in the GitHub secrets to connect to Azure Blob container to test upload/retrieve profile images.

### 4. Run server

```
python manage.py runserver
```

### 5. Test (Using Talend API Tester - Chrome extension)

#### User Account Management

1. User register
   - URL: http://127.0.0.1:8000/users/create/
   - Method: POST
   - Request Header:
     Content-Type: application/json
   - Request Body:
     ```
     {
       "fullname": "test",
       "email": "test@example.com",
       "age": 25,
       "password": "123456"
     }
     ```

2. User login
   - URL: http://127.0.0.1:8000/users/login/
   - Method: POST
   - Request Header:
     Content-Type: application/json
   - Request Body:
     ```
     {
       "email": "test@example.com",
       "password": "123456"
     }
     ```
   - Response:
     After successfully logged in, two tokens (refresh token and access token) will be returned in the response body.

3. User logout
   - URL: http://127.0.0.1:8000/users/logout/
   - Method: POST
   - Request Header:
     Content-Type: application/json
   - Request Body:
     ```
     {
       "refresh": "<refresh token>"
     }
     ```

4. Retrieve user's info
   - URL: http://127.0.0.1:8000/users/get-user-info/
   - Method: GET
   - Request Header:
     Authorization: Bearer <access token>
   - Response Body: (json file)
     For example:
     ```
     {
       "refresh": "<refresh token>"
     }
     ```

5. User update
   - URL: http://127.0.0.1:8000/users/update/
   - Method: POST
   - Request Header:
     Content-Type: application/json
     Authorization: Bearer <access token>
   - Request Body:
     ```
     {
       "fullname": "<new-name>",
       "email": "<new-name>@example.com",
       "age": <new-age>,
       "bio": "This is my bio."
     }
     ```

6. User account delete
   - URL: http://127.0.0.1:8000/users/delete/
   - Method: DELETE
   - Request Header:
     Content-Type: application/json
     Authorization: Bearer <access token>

7. User change password
   - URL: http://127.0.0.1:8000/users/change-password/
   - Method: PUT
   - Request Header:
     Content-Type: application/json
     Authorization: Bearer <access token>
   - Request Body:
      ```
      {
        "old_password": "123abc",
        "new_password": "123456",
        "confirm_new_password": "123456"
      }
      ```

      > **_Note:_** Don't use too simple password (at least 6 characters) when you call `change_password` API. 


#### Profile Image Management

8. Upload profile image
   - URL: http://127.0.0.1:8000/users/upload-profile-image/
   - Method: PUT
   - Request Header:
     Content-Type: multipart/form-data
     Authorization: Bearer <access token>
   - Request Body (Form):
     Name: profile_image
     Type: File
     Choose a file: <the image to upload>
   - Response Body: 
     image_url returned in the response body when uploading suceeded.
     


9. Retrieve profile image
   - URL: http://localhost:8000/users/retrieve-profile-image/
   - Method: GET
   - Request Header:
     Authorization: Bearer <access token>
   - Response Body: 
     image_url returned in the response body when uploading suceeded.


#### User interest selecting

10. Interest list (for frontend dropdown list)
   - URL: http://localhost:8000/users/get-interest-list/
   - Method: GET
   - No headers (no credential required)
   - Response Body: 
     A list of key:value pairs, such as:
     ```
      [
      {
      "value": "sports",
      "label": "Sports"
      },
      {
      "value": "music",
      "label": "Music"
      },
      {
      "value": "tech",
      "label": "Technology"
      },
      {
      "value": "art",
      "label": "Art"
      },
      {
      "value": "travel",
      "label": "Travel"
      }
      ]
     ```

11. (Users) Interest select
   - URL: http://localhost:8000/users/update-interest/
   - Method: POST
   - Request Header:
     Content-Type: application/json
     Authorization: Bearer <access token>
   - Request Body:
     ```
     {
       "interest": "<user's interest>"
     }
     ```

12. Get user's interest
   - URL: http://localhost:8000/users/retrieve-interest/
   - Method: GET
   - Request Header:
     Content-Type: application/json
     Authorization: Bearer <access token>
   - Response Body: 
     (The user's) interest returned in the response body.


13. Get a list of users with the same interest
   - URL: http://localhost:8000/users/get-recommend-matchups/
   - Method: POST
   - Request Header:
     Content-Type: application/json
   - Request Body:
     ```
     {
       "interest": "<an interest>"
     }
     ```
   - Response Body: 
     (The user's) interest returned in the response body.

