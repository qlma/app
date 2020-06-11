# Qlma - and the message gets delivered

Communication between school and home requires better services.

## Start development environment
```bash
docker-compose up
```

## load testdata from fixture
```bash
docker exec -it web_container python manage.py loaddata testdata_en
```