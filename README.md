# Bitly Alter
This is a platform capable of generating short URLs for big looooong URLs;
Also, Auto-Redirection is available.

## Install Dependencies
Clone repo, move to project root directory, and then execute:
```
pip install -r requirements.txt
```

## Initial Database
```
sudo su - postgres (enter the password, if it's the first time enter <mark>postgres</mark> as password)
psql
CREATE DATABASE bitly_alter;
```

## Run Platform (In Development Environment) 
Move to project root directory and then execute:
```
sh .entrypoint
```

## Tech

Bitly Alter uses several open-source projects to work properly:

* Flask
* Redis
* PostgreSQL
