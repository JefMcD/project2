# README 

## Prep

### Create Virtual Environment

cd /path-to-parent-folder-of-project-root/
python3 -m venv .venv
source .venv/bin/activate

## Packages to install

### Essential

* django
* python-decouple

pip3 install django 
pip3 install python-decouple 


### For Deployment to Production 
* whitenoise
pip3 install whitenoise 


###To Use MySQL DB (instruction for Ubuntu 22.04.02)###
* pkg-config
* python3-dev default-libmysqlclient-dev build-essential
* mysqlclient

sudo apt install mysql-server -y
sudo mysql_secure_installation
sudo apt-get update
sudo apt-get install pkg-config -y

sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

pip install mysqlclient

### Configure DATABASES in settings.py
// Connecting MySQL
// https://stackoverflow.com/questions/19189813/setting-django-up-to-use-mysql

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


### Additional Debug Info
* django-debug-toolbar
See Django Debug Toolbar Documentation

# Assessment Video
## Video Testing Requirements for Assessment
 [https://rumble.com/v37lw8a-project2-commerce.html](https://rumble.com/v37lw8a-project2-commerce.html).



### Assessment Video Timestamps

https://rumble.com/v388v5s-cs50-project-2-commerce.html



## RQ. 1 Models (0:00)
1. The Database has 7 entities, 6 models and 1 M2M field which is contained in the User Model 

## RQ. 2 Create Listing Test. (0:39) 
1.	Metal Zone
	https://i.imgur.com/jkeDHx3.jpeg
	Everything you need to sound exacly like Eddie Van Halen

	Title, Description, Starting Bid, Image, Category, Condition 

## RQ.3 Test Active Listings Page (0.25)
		
1. Default Route shows all the current Active Listings
		Displaying; Title, Description, Current Price, Photo 

## RQ.4 Listing Page Test
			
1. Clicking a listing goes to that page, showing details for that item (1.00)


2.	Add Item To Watchlist (1.38)
	Remove Item From Watchlist (1.45)
3.	Bid Lower than starting price On Item - Presented Error (2.05)
	Bid lower than high Bid on item - Presented Error (2.16)
	Bid Higher - Message (2.23)
4.	Close The Auction  (1:17)
5. 	Win Auction and Load Listing Page -  Message ‘You Won’ (2.30)
6. 	Add Comment to Listing (2.58)
7. 	Display All Comments (3.05)

## RQ.5 Watchlist Test
		
1. Add Items to Watchlist (1.35)
2. Open Watchlist Page to SHow (1:35)
3. Click Watchlist Item goes to that page (1.35)

## RQ.6 Categories Test (3.10)
		
1. Users can display a list by category 

## RQ.7  Django Admin Test (3.35)
		
1. Superuser can add, edit and delete listings, comments and bids on the site 