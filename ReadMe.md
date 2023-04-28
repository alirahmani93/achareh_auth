# Authentication app with Ip and mobile_number Blocking

### Author:

Ali Rahmani & email: ali93rahmani@gmail.com

# Important item in .env file

```
SECRET_KEY
DEBUG
ALLOWED_HOSTS
PROJECT_NAME
GUNICORN_WORKERS
GUNICORN_TIMEOUT
GUNICORN_PORT
```

# Deployment

1- Run command:

> docker-compose up -d

2- Type in browser:

> http://localhost:8000  [GET]

3- Step 1: user enter mobile number and get next step link:

> http://localhost:8000/api/auth/exists/  [POST]

4- Step 2: if user already exists

> http://localhost:8000/api/auth/login/  [POST]

5- Step 3: If user not exists and get next step link

> http://localhost:8000/api/auth/otp/verify/  [POST]

6- Step 4: User register and update data

> http://localhost:8000/api/auth/register/   [POST]

### Also, you can check system health and get application data

7- health check

> http://localhost:8000/api/app/health/  [GET]

8- application data

> http://localhost:8000/api/app/  [GET]


9- For test:

> python manage.py test