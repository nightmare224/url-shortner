# url-shortner
URL shortener for UVA project

## Installation
To run the project locally, after cloning, install all the dependencies.
```
pip install -r requirements.txt
```
Then get inside flaskr dir
```
cd flaskr
```
## How to spin-up docker compose

run the following command, api and database should be able to spin-up

```
docker-compose up --build --force-recreate
```

After successful, you should be able to connect to postgres db

```
host: 127.0.0.1
port: 5432
user: postgresadmin
password: admin123

```

Also you should be able to make api calls on your localhost