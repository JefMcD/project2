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
Timestamps for Video
https://rumble.com/v388v5s-cs50-project-2-commerce.html

	RQ. 1 Models
0:00	The Database has 7 entities, 6 models and 1 M2M field which is contained in the User Model

	RQ. 2 Test.
0:39		Create Listing
		Metal Zone
		https://i.imgur.com/jkeDHx3.jpeg
		Everything you need to sound exacly like Eddie Van Halen

		Title, Description, Starting Bid, Image, Category, Condition

	RQ.3 Test
0.25		Active Listings Page
		1. Default Route shows all the current Active Listings
		Displaying; Title, Description, Current Price, Photo

	RQ.4 Test
1.00		Listing Page	
		Clicking a listing goes to that page, showing details for that item


1.38		1.	Add Item To Watchlist
1.45			Remove Item From Watchlist
2.05		2.	Bid Lower than starting price On Item - Presented Error
2.16			Bid lower than high Bid on item - Presented Error
2.23			Bid Higher - Message
1:17		3.	Close The Auction 
2.30		4. 	Win Auction and Load Listing Page -  Message ‘You Won’
2.58		5. 	Add Comment to Listing
3.05		6. 	Display All Comments

	RQ.5 Test
		Watchlist
1.35		Add Items to Watchlist
1:35		Open Watchlist Page to SHow
		
1.35		Click Watchlist Item goes to that page

	RQ.6 Test
		Categories
3.10		Users can display a list by category

	RQ.7  Test
		Django Admin
3.35		Superuser can add, edit and delete listings, comments and bids on the site