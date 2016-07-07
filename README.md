# hack-pineapple

## Init dev environment
- create virtual enviroment for project `virtualenv venv-pineapple`
- avctivate virtual environment. `venv-pineapple\Scripts\activate.bat` - Win OS, `. venv-pineapple/bin/activate` - Linux/MAcOS
- install requirements. In activated virtual environment do `pip install -r requirements.txt`

## Make migrations and migrate
- in project root dir do `cp tools\makemigrations.py .` and then `python makemigrations.py`
- migrate structure to DB `python manage.py migrate`

## Run server
- in project root dir do `python manage.py runserver 0.0.0.0:80`

## Open app
- open app in browser [http://127.0.0.1]