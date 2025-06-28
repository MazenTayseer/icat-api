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
