 # library-api

### Project Description:
    In this project was implemented an online management system for book borrowings. The system optimizes the work 
    of library administrators and  makes the service much more user-friendly.
    
### Components:
    
    Books Service:
    Managing books amount (CRUD for Books)
    API:
    POST:                api/books/              - add new (only admin) 
    GET:                 api/books/              - get a list of books
    GET:                 api/books/<id>/         - get book's detail info (admin and authenticated)
    PUT/PATCH:           api/books/<id>/         - update book (also manage inventory, only admin) 
    DELETE:              api/books/<id>/         - delete book (only admin)
    
    Users Service:
    Managing authentication & user registration
    API:
    POST:           api/users/register/                   - register a new user 
    POST:           api/users/token/             - get JWT tokens 
    POST:           api/users/token/refresh/     - refresh JWT token 
    GET:            api/users/me/                - get my profile info 
    PUT/PATCH:      api/users/me/                - update profile info 
    
    Borrowings Service (FOR Authenticated):
    Managing users' borrowings of books
    API:
    GET:              api/borrowings/                             - list of borrowings (for all users if user=admin and list of your borrowings if you are not admin)
    POST:             api/borrowings/   		                  - add new borrowing (when borrow book - inventory should be made -= 1
                                                                you have to choose book, and expected_return_date, but you may not provide expected_return_date,
                                                                by default it will be 2 weeks.)
    GET:              api/borrowings/?user=...&is_active=true     - get borrowings by user id and whether is borrowing still active or not. For non admin users, you can
                                                                use only ?is_active=true
    GET:              api/borrowings/<id>/  			          - get specific borrowing 
    POST: 	          api/borrowings/<id>/return/ 		          - set actual return date (inventory should be made += 1)
    
    Notifications Service (Telegram):
    Notifications about new borrowing created.
    Other services interact with it to send notifications to library administrators.
    Usage of Telegram API, Telegram Chats & Bots.


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
pip install -r requirements.txt
create .env and fill it with necessary env variables

  **Please note**: 
  -BOT_TOKEN=6081832957:AAH2nu93PXRGmtjEMVNKBel7G2beHF2sKk8(test_bot_library)
  -СHAT_ID=it is your telegram`s id. You can find it by Get My ID telegram bot.(https://t.me/getmyid_bot)

python manage.py migrate
python manage.py runserver 
```
### Admin credentials:
    e-mail: admin@example.com
    password: test_admin12345

### Features
    - Permissions implemented
    - CRUD for books
    - Borrowing and return mechanism with books amount accounting
    - Notification for admin about new borrowing via Telegram bot
    - Daily notification for admin about overdue borrowings

    
    