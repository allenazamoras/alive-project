# aLive

A livestreaming app that lets you create and accept requests for other users. The more requests you complete the more reputation points you can achieve as a proactive and outstanding app user

## Getting Started
Follow these steps to get this project to run on you local machine for development and testing purposes.

### Prerequisites
This project will require the use of the following:

* [Python](https://www.python.org/downloads/) (3.5 or higher)
* [Django](https://docs.djangoproject.com/en/2.0/intro/install/) (2.0 or higher)
* [NodeJS](https://nodejs.org/en/download/) (8.x or higher)
* [OpenTok API](https://tokbox.com/developer/)

### Installation Guides

Clone this repository

```
$ git clone https://github.com/ephraimeg/alive-project
```

#### Set up a virtual enviroment:  
You can name your environment however you like, for this example we will use 'env'

```
$ python3 -m venv env
$ source env/bin/activate
```  

You can exit from the virtual environment at any time by typing

```
$ deactivate
```

#### Installing requirements:

Move to the directory `alive-project/` where you can find a file named `requirements.txt` then enter this command:

```
$ pip install -r requirements.txt
```

If `pip` is not installed on your machine you can follow the instructions [here](https://pip.pypa.io/en/stable/installing/)

#### Set up the database:

Set up Postgresql using this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04) from Digital Ocean

```
$ pip install psycopg2
$ sudo su - postgres
psql
```

You are now logged into a Postgres session, let's create your database:

**DO**: choose a meaningful name for your database

```
CREATE DATABASE mydatabase;
CREATE USER myprojectuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
exit
```

####local_settings.py
Sensitive information stored in the `local_settings.py` are as follows

```
API_KEY = 'OpenTokApiKey'
OT_SECRET_KEY = 'OpenTokSecretKey'

DATABASE_NAME = 'mydatabase'
DATABASE_USER = 'myprojectuser'
DATABASE_USER_PASSWORD = 'password'
DATABASE_HOST = 'localhost'
DATABASE_PORT = ''
```

## Deployment

## Contributing

## Versioning

## Authors
* Gao, Michael
* Godinez, Ephraime
* Zamoras, Allena

## License

## Acknowledgements
* To our mentors: 
 - Navarro, Aldrin
 - Tumulak, Jonathan
