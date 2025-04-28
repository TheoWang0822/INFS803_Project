# Backend Development Guide

1. Fetch Github resprepository in local
2. Run below commands
```cmd
cd server/
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install django djangorestframework
cd weather_api/
python manage.py runserver
```
3. Access http://127.0.0.1:8000/getStatus