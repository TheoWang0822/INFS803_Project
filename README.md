# Backend Development Guide

### Setup

1. Fetch Github resprepository in local
2. Run below commands
```cmd
cd server/
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install django djangorestframework
cd weather_api/
pip install -r requirements.txt
```
3. Run below commands
```cmd
python manage.py runserver
```
Access http://127.0.0.1:8000/getStatus

---

### Initialize City List

1. Run below commands
```cmd
cd /server/weather_api/tool/
python initialize_citylist.py
```

---

### How to check SQLite data

1. Run below commands
```cmd
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
sqlite3 db.sqlite3
.tables # Check all the tables
.headers on # show column name
```
```sql
select * from api_citylist limit 10; #Check top 10 cities from citylist table
```
