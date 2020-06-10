{\rtf1\ansi\ansicpg1252\cocoartf2511
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Working with Postgres container\
\
## list tables\
\'b4\'b4\'b4bash\
docker exec -it postgres_container psql -Upostgres -a postgres -c '\\l'\
\'b4\'b4\'b4\
\
## query\
\'b4\'b4\'b4bash\
docker exec -it postgres_container psql -U postgres -a postgres -c 'SELECT * FROM posts;'\
\'b4\'b4\'b4\
\
## backup\
\'b4\'b4\'b4bash\
docker exec -it postgres_container pg_dump -U postgres --column-inserts --data-only postgres > qlmadb/backup.sql\
\'b4\'b4\'b4\
\
## migrate\
\'b4\'b4\'b4bash\
docker exec -it web_container python manage.py makemigrations\
docker exec -it web_container python manage.py migrate\
\'b4\'b4\'b4\
\
## create super user\
\'b4\'b4\'b4bash\
docker exec -it web_container python manage.py createsuperuser\
\'b4\'b4\'b4\
\
## load initial data from fixture data.json\
\'b4\'b4\'b4bash\
docker exec -it web_container python manage.py loaddata testdata}