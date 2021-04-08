# Qlma

Communication between school and home requires better services.

## Local development environment

### Start containers
```bash
docker-compose up
```

### load testdata from fixture
```bash
docker exec -it web_container python manage.py loaddata testdata_en
```

### Run functional tests
```bash
docker exec -it web_container python manage.py test --debug-mode
```

## Heroku

### Deploy from IDE
```bash
git add .
git commit -m "Heroku setup"
git push heroku master
```

## Prepare application
```bash
heroku run python manage.py collectstatic
heroku run python manage.py migrate
```

## load testdata from fixture
```bash
heroku run python manage.py loaddata testdata_en
```