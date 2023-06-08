# Bababos Backend Engineer Test

this project is for backend engineer test

## Objective of this project:

Based on the problem statement, create a proposed solution with:

- [ ] The application must first log in using a Google Account (optional but is a plus)

- [ ] A clear and detailed description of your flow of the logic (you can use Miro or Google
Slide or any other tools that you are comfortable with)

- [X] You are showcasing your logic in your coding. It doesn’t have to be a full-fledged
tool/system, as long as we can try and run sets of data to check the algorithms, it’s
enough.

The project should be built with security, performance, and scalability in mind, and the code
should be well-organized, well-documented, and follow industry best practices. This mini
project is designed to be able to be done within no more than 3 days of work.

## Technical Requirements
- [x] Backend should be built using a modern programming language such as Python (is a
plus) or Golang.

- [x] Use of any suitable backend framework such as Flask, Django and any other
relevant framework.

- [x] Use a Relational database management system (RDBMS) such as MySQL or
PostgreSQL.

- [x] Create database tables for storing data related to problems and any other relevant
information.

- [x] Develop a RESTful API to allow users to submit and retrieve data through HTTP
requests.

- [ ] Deploy it on cloud infrastructure such as AWS, GCP, Vercel, Heroku, Qovery, and
any other relevant cloud infrastructure (optional but is a plus).

- [ ] Write a set of unit tests that cover the major functionalities and ensure proper
handling of edge cases.


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