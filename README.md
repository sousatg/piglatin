# Piglatin API

## Built With

- Flask
- Flask-JWT-Extended
- SQLAlchemy
- Gunicorn
- Postgres
- Redis

## Features

- API rate limited (user rate)
- Token based authentication (JWT)
- Logging
- Instrumentation with Prometheus
- API Documented with OpenAPI

## Installation

### Setup

Follow the following directions for clonning the repository and installing requirements.

#### What you'll need

- Git
- Docker
- Docker-Compose

#### Clone the Repository

```
git clone https://
```

#### Change directories into the main project folder

```
cd piglatin
```

### Local Development Setup

Create a `.env` file at the root folder with the following environment variables:

- `PORT` - Piglating running port.
- `DEBUG_PORT` - Piglating debugpy running port (use to debu with VSCode)
- `DEBUG` - Is the application running in debug mode or not (True/False)
- `DATABASE_ENGINE` -
- `DATABASE_NAME` - A pre created database in our Postgres instance
- `DATABASE_USER` - A user with previledges to the database
- `DATABASE_PASSWORD` - The database user password
- `DATABASE_PORT` - Port used to connect to our database
- `DATABASE_HOST` - The Postgres database host our app will connect
- `MAIL_SERVER` - Address of the email server
- `MAIL_PORT` - Port used by the email server
- `JWT_SECRET_KEY` - The key used for the JWT tokens

#### Start the project

1. Build the docker images using `docker-compose build`.
2. At the root folder run `docker-compose up -d`.
3. Make sure all images are running with `docker ps`.

### Useful commands

- `make tests` - will run the django tests
- `make bash` - runs `docker-compose exec blog bash`
