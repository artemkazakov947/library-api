 # library-api

### Project Description:
    In this project was implemented an online management system for book borrowings. The system optimizes the work 
    of library administrators and  makes the service much more user-friendly.
    
### Functional (what the system do):
    Web-based
    Manage books inventory
    Manage books borrowing
    Manage customers
    Display notifications

## Installing / Getting started

You have to install Python 3.
 
```shell
git clone https://github.com/artemkazakov947/library-api.git
cd library_api
python -m venv venv
venv\Scripts\activate
pip install -r requirementes.txt
create .env and fill it with necessary env variables

  **Please note**: 
  -BOT_TOKEN=6081832957:AAH2nu93PXRGmtjEMVNKBel7G2beHF2sKk8(test_bot_library)
  -СHAT_ID=it is your telegram`s id. You can find it by Get My ID telegram bot.

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 
```

### Features
    - Permissions implemented
    - CRUD for books
    - Borrowing and return mechanism with books amount accounting
    - Notification for admin about new borrowing via Telegram bot

    
    