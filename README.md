# django login system

## How to run in linux:


```
Go to project folder:
```
cd lootadda
```
Create a Virtual Environment:
```
python3 -m venv venv
```
Activate Virtual Environment:
```
source venv/bin/activate
```
Install Requirements Package:
```
pip install -r requirements.txt
```
Migrate Database:
```
python manage.py migrate
```
Create Super User:
```
python manage.py createsuperuser
```
Finally Run :
```
python manage.py runserver
```
It will start a local server on 'http://127.0.0.1:8000'

then go to http://127.0.0.1:8000/admin to accesss your administrations.
