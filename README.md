# Chatbubble
Chatbubble is a one-to-one private messaging app allowing users to send and receive text and 
photo messages in real-time with other users.

<img width="949" alt="image" src="https://user-images.githubusercontent.com/110189117/210552093-fdce20cc-40c0-48d5-bf42-63b757d412cc.png">
<img width="959" alt="image" src="https://user-images.githubusercontent.com/110189117/210553740-edea10b6-9ef9-4f9c-ba86-079b012855f7.png">

# Getting started

## Installing pip
1. https://pypi.org/project/pip/ </br>
2. Open cmd prompt </br>
3. `pip install pip`

## Creating your virtual environment
1. Open cmd prompt </br>
2. `python -m venv env`

## Installing requirements
1. Open cmd prompt </br>
2. `pip install -r requirements.txt`

## Postgres Setup
Postgres needs to run as a service on your machine. Since I'm using windows I will show you how to do this on windows.
</br> </br>
1. Download postgres: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads</br>
2. run the .exe file and go through the installation</br>
  i. remember the superuser password you use. This is very important.</br>
  ii. port 5432 is the standard</br>
3. After installation confirm the service is running by opening the "Services" window on windows.</br>
4. Confirm you have access to database.</br>
  i. open cmd prompt</br>
  ii. write `psql postgres postgres`</br>
    * means: "connect to the database named 'postgres' with the user 'postgres'". 'postgres' is the default root user name for the database.</br>
5. Some commands you'll find useful:</br>
  i. List databases</br>
    * `\l`</br>
  ii. Connect to a different database</br>
    * `\c databasename`</br>
    * Keep in mind you will not have any other databases. We will create one in a second.</br>
  iii. List the tables in a database.</br>
    * `\dt`</br>
  iv. create a new database for our project</br>
    * `CREATE DATABASE chatbubbledb;`</br>
  v. Create a new user that has permissions to use that database</br>
    * `CREATE USER django WITH PASSWORD 'password';`</br>
    * These credentials are important to remember because they are used in the django postgres configuration.</br>
  vi. List all users</br>
    * `/du`</br>
  vii. Give the new user all privileges on new db</br>
    * `GRANT ALL PRIVILEGES ON DATABASE chatbubbledb TO django;`</br>
  viii. Test</br>
    a. disconnect from db</br>
      * `\q`</br>
    b. Connect to the db with user</br>
      * `psql chatbubbledb django`</br>

## Creating the .env file
Next we will need to create a .env file in the same folder as our settings.py file. Your .env file should be structured like this:</br>
```
SECRET_KEY=your-secret-key
DATABASE_NAME=chatbubbledb
DATABASE_USER=django
DATABASE_PASS=password

SMTP_EMAIL=your-email
SMTP_PASSWORD=your-email-password
```
To generate a secret key you'll need to:</br>
1. Open cmd prompt.</br>
2. `python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

## Starting Redis

## Starting your server
