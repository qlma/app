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
docker exec -it web_container python manage.py test --debug-mode --verbosity 2
```

### View browser execution while tests run
Connect with vnc to the browsers (0.0.0.0:6900 and 0.0.0.0:6901). 
When prompted for password the default is secret.

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
heroku run python manage.py makemigrations
heroku run python manage.py migrate
```

## load testdata from fixture
```bash
heroku run python manage.py loaddata testdata_en
```