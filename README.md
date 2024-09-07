# Run guide #
git clone https://github.com/Mars687p/test_cdn.git
python -m venv env && source env/Scripts/activate.bat
Заполнить .env file
pip install -r requirements.txt
Установить PostgreSQL
Установить Postgis и выполнить следующие команды в БД:
    CREATE EXTENSION postgis;
    CREATE EXTENSION btree_gist;

python3 manage.py runserver