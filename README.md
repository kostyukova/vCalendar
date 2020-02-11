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
