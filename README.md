#README

##Prep

###Create Virtual Environment
$ cd /path-to-parent-folder-of-project-root/
$ python3 -m venv .venv
$ source .venv/bin/activate

##Packages to install

###Essential
*django
*python-decouple

$ pip3 install django 
$ pip3 install python-decouple 


###For Deployment to Production 
*whitenoise
$ pip3 install whitenoise 


###To Use MySQL DB (instruction for Ubuntu 22.04.02)
*pkg-config
*python3-dev default-libmysqlclient-dev build-essential
*mysqlclient

$ sudo apt install mysql-server -y
$ sudo mysql_secure_installation
$ sudo apt-get update
$ sudo apt-get install pkg-config -y
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
$ pip install mysqlclient

###Configure DATABASES in settings.py
# Connecting MySQL
# https://stackoverflow.com/questions/19189813/setting-django-up-to-use-mysql

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': database-name
        'USER': user-name,
        'PASSWORD': password,
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
        },
    }
}


###Additional Debug Info
*django-debug-toolbar
See Django Debug Toolbar Documentation

#Assessment Video
##Video Testing Requirements for Assessment
 [https://rumble.com/v37lw8a-project2-commerce.html](https://rumble.com/v37lw8a-project2-commerce.html).



###Assessment Video Timestamps
Project2 – Commerce Timestamps

RQ. 1 
**Models**
0:00 The Database has 7 entities, 6 models and 1 M2M field

RQ. 2 Test.
0:20 
**Create Listing**
Metal Zone
https://i.imgur.com/jkeDHx3.jpeg
Everything you need to sound exacly like Eddie Van Halen

Title, Description, Starting Bid, Image, Category, Condition

RQ.3 Test
0.28 
**Active Listings Page**
1. Default Route shows all the current Active Listings
Displaying; Title, Description, Current Price, Photo

RQ.4 Test
0.35 
**Listing Page**
Clicking a listing goes to that page, showing details for that item

(Start Not Signed In)
Page has additional functionality available when a user is signed in.
(sign in turkle)

0:40 1. Add Item To Watchlist
0:45 Remove Item From Watchlist
0:49 2. Bid Lower than starting price On Item - Presented Error
0:59 Bid lower than high Bid on item - Presented Error
Bid Higher - Message
1:08 3. Close The Auction
1:21 4. Win Auction and Load Listing Page - Message ‘You Won’
1:25 5. Add Comment to Listing
1:30 6. Display All Comments

RQ.5 Test
**Watchlist**
1:40 Add Items to Watchlist
1:45 Open Watchlist Page to SHow

0:41 Click Watchlist Item goes to that page

RQ.6 Test
**Categories**
1:56 Users can display a list by category

RQ.7 Test
**Django Admin**
2:25 Superuser can add, edit and delete listings, comments and bids on the site

