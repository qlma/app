# Working with Postgres container

## list tables
``` bash
docker exec -it postgres_container psql -Upostgres -a postgres -c 'l'
```

## query
``` bash
docker exec -it postgres_container psql -U postgres -a postgres -c 'SELECT * FROM posts;'
```

## backup
``` bash
docker exec -it postgres_container pg_dump -U postgres --column-inserts --data-only postgres > qlmadb/backup.sql
```

## migrate
``` bash
docker exec -it web_container python manage.py makemigrations
docker exec -it web_container python manage.py migrate
```

## create super user
``` bash
docker exec -it web_container python manage.py createsuperuser
```

## load testdata from fixture
``` bash
docker exec -it web_container python manage.py loaddata testdata_en
```