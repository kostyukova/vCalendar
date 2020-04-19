# Vacation calendar system

## To create database
```
mysql -u root -p < sql/mysql_db.sql
```

## To create tables and sample data
```
mysql -u vcalendar_user -p vcalendar < sql/mysql_data.sql
```
## To generate backend api stub
```
java -jar swagger-codegen-cli-2.4.10.jar generate  -i swagger_vcalendar.yaml -l python-flask -o backend
```

## To generate backend api stub
```
java -jar swagger-codegen-cli-2.4.10.jar generate  -i swagger_vcalendar.yaml -l typescript-angular -o frontend/src/app/api_client
```

## To launch backend localy
cd ./vCalendar
pipenv shell
cd ./backend 
python -m swagger_server
-- backend API will be available at http://localhost:8080/vcalendar/ui

## To launch frontend localy in dev mode
cd ./frontend
ng serve | ng serve --prod
ng build --prod | npm run build:production

## To launch backend like docker container
cd ./backend
docker build -t vcalendar-backend:V1.0 .
docker run -p 8080:8080 -d vcalendar-backend:V1.0

## To launch fronend like docker container
cd ./frontend
docker build -t vcalendar-frontend:V1.0 .
docker run -p 8081:80 -d vcalendar-frontend:V1.0

## Push docker images to github repository
docker login -u kostyukova -p TOKEN docker.pkg.github.com
docker images | docker image ls
docker tag c5db16ad6fcb docker.pkg.github.com/kostyukova/vcalendar/vcalendar-backend:V1.0
docker tag 62553c804d29 docker.pkg.github.com/kostyukova/vcalendar/vcalendar-frontend:V1.0
docker push docker.pkg.github.com/kostyukova/vcalendar/vcalendar-frontend:V1.0
docker push docker.pkg.github.com/kostyukova/vcalendar/vcalendar-backend:V1.0

## Launch application with Docker Compose
docker-compose up
docker-compose down 