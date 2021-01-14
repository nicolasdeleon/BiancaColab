# Bianca's Back End


[![CircleCI](https://circleci.com/gh/nicolasdeleon/BiancaColab.svg?style=shield&circle-token=f6d6a58ac2745ac3a06ed8dab85299b7cd59c3c8)](<LINK>)


## Requirements

- Python 3.7.5
- You will need a secret **.env** file to access keys and tokens.
- PostgreSQL

## Getting Started (without docker - no prod)

You will need a secret **.env** file to access keys and tokens.

1. `python3 -m venv env` to generate a virtual environment for the project
2. `source env/bin/activate` to activate virtual environment
3. Inside virtual env: `pip install -r requirements.txt` to install all necessary packages
4. Make sure you have a postgres database created that matches the one in .env
5. Make sure .env variable PROD is set to False

Helpfull commands ([PosgreSQL_GetStarted](https://www3.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html)):

- `sudo -u postgres -i`
- `dropdb [DB NAME]`
- `createdb [DB NAME]`
- `psql` (to activate interactive PostgreSQL client as user postgres if previous command)
    - \l (list db)
- `psql databasename < data_base_dump`

5. Apply migrations `python manage.py makemigrations`
6. Apply dump
7. Run `python manage.py runserver`

## Getting Started Docker - Prod

1. Make sure .env variable PROD is set to True and .env DB_NAME is correctly set to db service
2. Run `docker-compose build`
3. Run `docker-compose up`
4. If you need to create a superuser, befor step 3:
    - Run `docker-compose run --rm --entrypoint bash bianca_web` this will create a container where you will have access to run `python manage.py createsuperuser` and this will be stored in the postgres db.
    - After this run step 3: `docker-compose up`
5. When finished: `docker-compose down`

Docker cheat sheet might help
