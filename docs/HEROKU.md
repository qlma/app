# Heroku

These instructions are for anyone who is configuring Qlma application in the Heroku Cloud.

## Deploy from IDE
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

# Postgres

## Query against Heroku Postgres database
```bash
heroku pg:psql -c "SELECT * FROM public.django_session;" --app "qlma"
```