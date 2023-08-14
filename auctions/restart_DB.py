
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from datetime import date
from .forms import *
from .models import *




def restart(request):
    return render(request, 'auctions/restart.html')

def reset(request):
    User.objects.all().delete()
    Health.objects.all().delete()
    Categories.objects.all().delete()
    Bids.objects.all().delete()
    
    auction_users = [
        {'username':'pepe', 'email': 'pepe@mail.com', 'password': 'passw0rd'},
        {'username':'turkle', 'email': 'turkle@mail.com', 'password': 'passw0rd'},
        {'username':'sheela', 'email': 'sheela@mail.com', 'password': 'passw0rd'},
        {'username':'bowfren', 'email': 'bowfren@mail.com', 'password': 'passw0rd'},
        {'username':'looda', 'email': 'looda@mail.com', 'password': 'passw0rd'},
        {'username':'smol', 'email': 'smol@mail.com', 'password': 'passw0rd'},
        {'username':'sparra', 'email': 'sparra@mail.com', 'password': 'passw0rd'},
    ]
    for user in auction_users:
        new_user = User.objects.create_user(user['username'], user['email'], user['password'])
        new_user.save()
        
    health = [
        {'description':'New'},
        {'description':'Mint'},
        {'description':'Very-Good'},
        {'description':'Good'},
        {'description':'Fair'},
        {'description':'Broken'},
    ]
    for condition in health:
        c = Health(description=condition['description'])
        c.save()
    
    categories = [
        {'description':'Furniture'},
        {'description':'Electronics'},
        {'description':'DIY'},
        {'description':'Clothing'},
        {'description':'Games'},
        {'description':'Music'},
        {'description':'Pets'},
        {'description':'Art'},
        {'description':'Books'},
    ]
    for category in categories:
        c = Categories(description=category['description'])
        c.save()
        
    # Health FKeys
    new = Health.objects.get(description='New')
    mint = Health.objects.get(description='Mint')
    good = Health.objects.get(description='Good')
    vgood = Health.objects.get(description='Very-Good')
    fair = Health.objects.get(description='Fair')
    broken = Health.objects.get(description='Broken')
   
   # Categories FKeys
    furn = Categories.objects.get(description='Furniture')
    elec = Categories.objects.get(description='Electronics')
    diy = Categories.objects.get(description='DIY')
    cloth = Categories.objects.get(description='Clothing')
    games = Categories.objects.get(description='Games')
    music = Categories.objects.get(description='Music')
    pets = Categories.objects.get(description='Pets')
    art = Categories.objects.get(description='Art')
    books = Categories.objects.get(description='Books')
    
    # User Fkeys
    pepe = User.objects.get(username='pepe')
    turkle = User.objects.get(username='turkle')
    sheel = User.objects.get(username='sheela')
    looda = User.objects.get(username='looda')
    smol = User.objects.get(username='smol')
    sparra = User.objects.get(username='sparra') 
    
    
    timestamp_now = datetime.now 
    active_listings = [
        { 
         'title' : 'Power Beenie', 
         'description' : 'Vikings wooly hat', 
         'image_url' : 'https://i.imgur.com/NR6YDvM.jpeg ', 
         'start_bid' : 5.00, 
         'listing_start' : datetime(2023, 8, 9, 00, 21, 38, 486910),  
         'listing_end' : datetime(2023,8,16,00,21,38,483198), 
         'category_fk' : cloth,
         'health_fk' : good , 
         'user_fk' : sparra 
         },
        
        { 
         'title' : 'Phaser', 
         'description' : 'Still working', 
         'image_url' : 'https://i.imgur.com/MobuKql.jpeg', 
         'start_bid' : 3.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'category_fk' : elec,
         'health_fk' : fair , 
         'user_fk' : pepe 
         },
        
        { 
         'title' : 'Weird Cat', 
         'description' : 'BioMechanical Cat Found at UFO Crash Site, seems to be trying to communicate', 
         'image_url' : 'https://i.imgur.com/NtDE1IS.jpeg', 
         'start_bid' : '230', 
         'listing_start' : datetime(2023,8,9,8,56,3,988426), 
         'listing_end' : datetime(2023,8,16,8,56,3,984790), 
         'category_fk' : pets, 
         'health_fk' : good , 
         'user_fk' : turkle 
         },
        
        {
         'title' : 'Pair of Socls', 
         'description' : 'One plain, one tartan. Small hole for big toe to go through', 
         'image_url' : '', 
         'start_bid' : '1', 
         'listing_start' : datetime.now(), 
         'listing_end' : datetime.now() + timedelta(days=7), 
         'category_fk' : cloth, 
         'health_fk' : vgood , 
         'user_fk' : turkle 
         }
    ]
    
    for listing in active_listings:
        l = Listings(title = listing['title'], 
                     description = listing['description'],
                     image_url = listing['image_url'],
                     start_bid = listing['start_bid'],
                     listing_start = listing['listing_start'],
                     listing_end = listing['listing_end'],      
                     category_fk = listing['category_fk'],
                     health_fk = listing['health_fk'],
                     user_fk = listing['user_fk']
                     )
        l.save()
        
    listing_bids = [
        {
            'bid': 5.00,
            'bid_time': datetime.now(),
            'listing_fk': None,
            'user_fk': pepe
        },
        
        {
            'bid': 3.00,
            'bid_time': datetime.now(),
            'listing_fk': None,
            'user_fk': looda
        },
                
        {
            'bid': 2.00,
            'bid_time': datetime.now(),
            'listing_fk': None,
            'user_fk': sparra
        }
    ]
        
    all_listings = Listings.objects.all()
    for listing in all_listings:
        for list_bid in listing_bids:
            b = Bids(bid = list_bid['bid'], bid_time = list_bid['bid_time'], listing_fk = listing.listing_id, user_fk = list_bid['user_fk'])
            b.save()
                
        
        

        
    listings = Listings.objects.all()
    all_bids = Bids.objects.all()
    bidform = bid_form()
    message='make a bid'
    return render(request, "auctions/index.html",{
                    'listings': listings,
                    'all_bids': all_bids,
                    'bid_form': bidform,
                    'error_message': message

    })
