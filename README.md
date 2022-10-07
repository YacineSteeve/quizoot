# Quizoot

## Project setup

1. Frontend

- Install npm dependencies using `yarn`.

```bash
$ cd frontend && yarn install && cd ..
```

2. Server

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

- To compiles and hot-reloads the frontend for development, run `yarn server`
- In another terminal, you can launch the django server with `python manage.py runserver` (assuming your virtual environment is activated).
