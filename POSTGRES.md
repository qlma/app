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
