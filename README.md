
## Способ запуска:

Самый простой способ познакомиться с PostgreSQL — запустить его в docker-контейнере. Для этого достаточно выполнить команду:
```docker
docker run -d --rm -p 5432:5432 --name postgres -v <pwd>/admin_psql_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=<secret_password> postgres:14
```

Подключитесь к контейнеру:
```docker
docker exec -it postgres bash
```

Теперь вы внутри контейнера. Чтобы попасть в PostgreSQL shell, наберите такую команду:
```sh
psql -U postgres
```

Для выхода из PostgreSQL shell введите ```\q```. Чтобы вернуться обратно на хост-машину, выполните команду ```exit```.

**Внутри PostgreSQL shell:**
* создайте базу
```sql
CREATE DATABASE movies;
```
* создайте пользователя
```sql
CREATE USER movies WITH PASSWORD 'movies';
```
* назначте права работы с базой, созданному пользователю
```sql
GRANT ALL PRIVILEGES ON DATABASE "movies" to movies;
```

После чего запустите SQL команды от лица созданного пользователя ```psql -U movies```, команды находятся в
```sh
/schema_design/db_schema.sql
```

> Если вы используете Macbook на процессоре M1, зависимости надо установить с помощью команды
```sh
arch -arm64 pip install -r requirements.txt --no-cache-dir
```

Создав таблицы, остается только перенести данные из Sqlite в Postgres, файл запуска находится в
```sh
/sqlite_to_postgres/load_data.py
```

Теперь можно запустить проект Django вместе с миграциями:
```vim
python manage.py migrate --fake-initial
or
python manage.py migrate --fake
```

Создаем супер пользователя и начинаем работать в админке:
```vim
python manage.py createsuperuser
```
```vim
python manage.py runserver
```

# Greetings traveller

Мы рады, что вы приступили к выполнению 1 задания из курса Middle Python-разработчик.

Описание структуры и порядок выполнения проекта:
1. `schema_design` - раздел c материалами для новой архитектуры базы данных.
2. `sqlite_to_postgres` - раздел с материалами по миграции данных.
3. `movies_admin` - раздел с материалами для панели администратора.

Успехов!
