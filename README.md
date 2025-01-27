# ICAT API

### MySQL

- Download `mysql` version 8.0.32 from [MySQL Installer Archives](https://downloads.mysql.com/archives/installer/)
- Add MySQL Server 8.0.32 and download it
- Make sure to set the `username:root` and `password:root`
- Download [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
- Run the following script in workbench
  ```sql
  CREATE DATABASE icat;
  ```

### Django

**RECOMMENDED: USE GIT BASH TERMINAL**

- Clone repo
- Make .venv
  ```bash
    python -m venv .venv
  ```
- activate .venv
  ```bash
    source .venv/Scripts/activate
  ```
- install requirements
  ```bash
    pip install -r requirements.txt
  ```
- migrate database files
  ```bash
    python manage.py migrate
  ```
- run app
  ```bash
    python manage.py runserver
  ```

### .env variables

- go to `.venv/Scripts/activate`
- scroll to the bottom and add
  ```bash
    export DATABASE_URL=mysql://root:root@127.0.0.1:3306/icat
    export ACCESS_TOKEN_LIFETIME=3600     # 1 hour
    export REFRESH_TOKEN_LIFETIME=604800  # 1 week
  ```
- every time you change the variables, you have to re-activate the env
  ```bash
    source .venv/Scripts/activate
  ```
