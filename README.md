
 # library-api

### Project Description:
    In this project was implemented an online management system for book borrowings. The system optimizes the work 
    of library`s administrators and  makes the service much more user-friendly.
    
### Functional (what the system do):
    Web-based
    Manage books inventory
    Manage books borrowing
    Manage customers
    Display notifications

## Installing / Getting started

You have to install Python 3 and create your own Telegram bot!


```shell
git clone https://github.com/artemkazakov947/library-api.git
cd library
pip install virtualenv venv
venv\Scripts\activate
pip install -r requirementes.txt
create .env and fill it with necessary env variables
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 
```

### Features
    - Permissions were implemented
    - CRUD for books
    - Borrowing and return mechanism with accounting of books amount
    - Notification for admin about new borrowing via Telegram bot

