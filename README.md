# Bitly Alter
This is a platform capable of generating short url for big agly looooong urls;
Also Auto-Redirection is available...

## Install Dependencies
Move to project root directory and then execute:
```
pip install -r requirements.txt
```

## Initial Database
```
sudo su - postgres (enter password)
psql
CREATE DATABASE bitly_alter;
```

## Run Platform (In Development Enviroment) 
Move to project root directory and then execute:
```
sh .entrypoint
```

## Tech

Bitly Alter uses a number of open source projects to work properly:

* Flask
* Redis
* PostgreSQL
