# hack-pineapple

## Init dev environment
- create virtual enviroment for project `virtualenv venv-pineapple`
- avctivate virtual environment. `venv-pineapple\Scripts\activate.bat` - Win OS, `. venv-pineapple/bin/activate` - Linux/MAcOS
- install requirements. In activated virtual environment do `pip install -r requirements.txt`

## set up database
- `CREATE DATABASE pineapple;`
- `CREATE USER pineapple WITH PASSWORD 'pineapple';`
- `GRANT ALL PRIVILEGES ON DATABASE pineapple TO pineapple;`

## Make migrations
- in project root dir do `cp tools\makemigrations.py .` and then `python makemigrations.py`

## Run server
- in project root dir do `python manage.py runserver 0.0.0.0:80`