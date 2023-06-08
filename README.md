# Bababos Backend Engineer Test

this project is for backend engineer test

## Tech Stack

**Server:** Python, Django, PostgreSQL, Docker

## Run Locally

Clone the project

```bash
  git clone https://github.com/wihlarkop/bababos-backend-engineer-test
```

Go to the project directory

```bash
  cd bababos-backend-engineer-test
```

you need set environment variable, you can see the example in .env-example

```dotenv
DATABASE_NAME=must-define
DATABASE_USER=must-define
DATABASE_PASSWORD=must-define
DATABASE_HOST=must-define
DATABASE_PORT=must-define
DEBUG=must-define
SECRET_KEY=must-define
```

### Install dependencies

there is two-way to install this project

first you can use docker for start server

```bash
docker-compose up -d --build
```

```bash
docker-compose exec api python manage.py migrate 
```

```bash
docker-compose exec api python manage.py createsuperuser 
```

second you can run manually

```bash
pip install -r requirements.txt
```

```bash
python manage.py migrate
```

```bash
python manage.py createsuperuser
```

```bash
python manage.py runserver
```

then you can open url at http://localhost:8000/