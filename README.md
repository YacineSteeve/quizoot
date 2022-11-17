# Quizoot

## Project setup

1. Frontend

- Install npm dependencies using `yarn`.

```bash
$ cd frontend && yarn install && cd ..
```

2. Server

- Create a new mongodb database, let's say `quizoot_db`.
  - If you have [MongoDB Compass](https://www.mongodb.com/docs/compass/master/install/), then launch it and:
    - enter the uri `mongodb://127.0.0.1:27017/` to connect to mongodb
    - create your database `quizoot_db` and a new collection `questions`
  - If you don't, then find a way to create a mongodb database yourself. ^-^

- Using the template `backend/.env.example`, create a new a file `backend/.env` file that looks like this:
  ```bash
  DATABASE_NAME=quizoot_db
  DATABASE_URL=mongodb://127.0.0.1:27017/quizoot_db
  ADMIN_PATH=/admin
  IN_PROD=false
  SECRET_KEY=some_long_enough_secret_key_here
  ```

- Create a virtual environment and activate it

```bash
$ python3 -m venv venv && source venv/bin/activate
```

- Install the requirements

```bash
$ pip install --upgrade pip && pip install -r requirements.txt
```

- Apply the migrations

```bash
$ python manage.py migrate
```

## Launch and run

- To compile and hot-reload the frontend for development, run `yarn dev`
- In another terminal, you can launch the django server with `python manage.py runserver` (assuming your virtual environment is activated).
