# Run guide #
1. git clone https://github.com/Mars687p/test_cdn.git
2. python -m venv env && source env/Scripts/activate.bat
3. Заполнить .env file
4. pip install -r requirements.txt
5. Установить PostgreSQL
6. Установить Postgis и выполнить следующие команды в БД:
   6.1 CREATE EXTENSION postgis;
   6.2 CREATE EXTENSION btree_gist;
7. python3 manage.py runserver