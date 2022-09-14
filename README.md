# fp_project


Steps:

### run mysql
docker-compose build mysql_db

docker-compose up mysql_db


### create db
docker exec -it mysql_db /bin/bash

bash-4.4### mysql -h localhost -u root -p

create database finance_peer;


### run web
docker-compose build web

docker-compose up web

### create super user
docker exec -it web /bin/bash

root@0232f7c93e22:/base_directory### python manage.py createsuperuser

### create normal user
go to localhost:8001/admin, login with superuser creds, create user

### test api
<pre>
curl --location --request POST 'localhost:8001/api/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": {username},
    "password": {password}
}'
</pre>

