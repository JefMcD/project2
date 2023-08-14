from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from .forms import *
from .models import *


def check_listing_is_watched(request, listing_pkey):
    # Find out if the listing is being watched by the user
    # then send is_watched status to the template so it can show a watch button or an unwatch button
    
    try:
        current_user = User.objects.get(username = request.user)
        watched_item = current_user.watchlist_m2m.get(listing_id = listing_pkey)
        if watched_item:
            is_watched = True
        
    except:
        # User not logged in, iten not being watched
        is_watched = False
    
    print(f" is_watched => {is_watched}")
        
    return(is_watched)

def check_user_is_high_bidder(request, listing_pkey):
    # determine if the user is the highest bidder on the listing
    # Whos is the highest bidder
    # Is the Highest bidder the User
    listing_details=Listings.objects.get(listing_id = listing_pkey)
    listing_bids = Bids.objects.filter(listing_fk = listing_details)
    try:
        high_bid_obj = listing_bids.latest('bid')
        high_bid_value = high_bid_obj.bid
        high_bid_user = high_bid_obj.user_fk
    except:
        # listing has no bids
        high_bid_value = 0.00
        high_bid_user = None
        
    if high_bid_user == request.user:
        user_is_high_bidder = True
    else:
        user_is_high_bidder = False
        
    return user_is_high_bidder


def get_this_listings_comments(request,listing_pkey):
    # Get all the comments for the listing
    try:
        comments_list = Comments.objects.filter(listing_fk = listing_pkey)
    except:
        # No Comments
        comments_list =  None
        
    return comments_list
  
def listing_page(request, listing_pkey):
    listing_details=Listings.objects.get(listing_id = listing_pkey)
    bidform = bid_form()
    new_comments_form = comment_form()
        
    is_watched = check_listing_is_watched(request,listing_pkey)
    user_is_high_bidder = check_user_is_high_bidder(request, listing_pkey)
    comments_list = get_this_listings_comments(request,listing_pkey)
    
    try:
        User.objects.get(username=request.user)
        if user_is_high_bidder:
            bid_message = 'You Are High Bidder!'
            if listing_details.is_active == False:
                bid_message = 'You Won!'
        else:
            bid_message = 'Place Your Bid!' 
    except:
        # No user logged in
        bid_message = 'Login or Register to Bid'

    return render(request, 'auctions/listing_page.html',{
                    'listing': listing_details,
                    'bid_form': bidform,
                    'bid_message': bid_message,
                    'is_watched': is_watched,
                    'user_is_high_bidder': user_is_high_bidder,
                    'comments_list': comments_list,
                    'comment_form': new_comments_form,
    })
  
  

def process_comment(request, listing_pkey):
    
    listing_details=Listings.objects.get(listing_id = listing_pkey)
    bidform = bid_form()
    new_comments_form = comment_form()
    
    user_listing = Listings.objects.get(listing_id=listing_pkey)
    comment_source = User.objects.get(username=request.user)
    print(f"user => ",comment_source)

    c = Comments(comment=request.POST['user_comment'], listing_fk = user_listing, user_fk = comment_source)
    c.save()
    
    is_watched = check_listing_is_watched(request,listing_pkey)
    user_is_high_bidder = check_user_is_high_bidder(request, listing_pkey)
    comments_list = get_this_listings_comments(request,listing_pkey)
        
    bid_message = 'Place Your Bid!' 
    return render(request, 'auctions/listing_page.html',{
                    'listing': listing_details,
                    'bid_form': bidform,
                    'bid_message': bid_message,
                    'is_watched': is_watched,
                    'user_is_high_bidder': user_is_high_bidder,
                    'comments_list': comments_list,
                    'comment_form': new_comments_form,
    })





def process_bid(request, bid_listing_id):

    # Get general page context
    listing_details=Listings.objects.get(listing_id = bid_listing_id)
    bid_user = User.objects.get(username = request.user)
    bidform = bid_form()
    new_comments_form = comment_form()
    
    is_watched = check_listing_is_watched(request,bid_listing_id)
    user_is_high_bidder = check_user_is_high_bidder(request, bid_listing_id)
    comments_list = get_this_listings_comments(request,bid_listing_id)
    
    
    print('##### process bid ####')
    print('bid_listing_id => ', bid_listing_id)
    #   Note: 
    #       objects.filter() returns a list that you need to iterate through to get to the record and attributes inside even if its only 1
    #       objects.get() returns only 1 record that allows you to directly access the attributes
    bid_listing = Listings.objects.get(listing_id=bid_listing_id)
    bidform= bid_form()
 

    # get max bid from bids table
    # max_bid = Bids.objects.aggregate(Max('bid'))
    # if table empty set max_bid to start_bid
    # else get max_bid from table

    high_bid = bid_listing.highest_bid() # looks at all the bids on a single listing and returns the one with the highest bid
    user_bid = float(request.POST['bid'])
    min_bid = float(bid_listing.start_bid)
    bid_message = 'Place Your Max Bid'
    # if user_bid > max_bid
    #   update max_bid and say Good Luck
    # else if user_bid < max_bid
    #   return form and say bid too low
    if user_bid > high_bid and user_bid >= min_bid:
        bid_listing_fk = Listings.objects.get(listing_id = bid_listing_id)
        user_bid_time = datetime.now()
        b = Bids(bid=user_bid, listing_fk = bid_listing_fk, user_fk = bid_user)
        b.save()
        
        bid_message = 'Good Luck!'        
    else:
        bidform = bid_form(request.POST)
        bid_message='Bid too low!'
        
    # Add Item to Users Watchlist    
    # If user not already watching item
    if not is_watched:
        bid_user.watchlist_m2m.add(bid_listing)
        is_watched = True
        
    return render(request, 'auctions/listing_page.html',{
                'listing': listing_details,
                'bid_form': bidform,
                'bid_message': bid_message,
                'is_watched': is_watched,
                'user_is_high_bidder': user_is_high_bidder,
                'comments_list': comments_list,
                'comment_form': new_comments_form,
    })
    


def login_view(request):
    new_login = login_form() 
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                'login_form': new_login,
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html", {
                        'login_form': new_login,
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    
    if request.method == "POST":
        new_registration = register_form()
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                        "message": "Passwords must match.",
                        'registration_form': new_registration
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                            "message": "Username/email already taken.",
                            'registration_form': new_registration
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        new_registration = register_form
        return render(request, "auctions/register.html",{
                        'registration_form': new_registration
        })
    

def create_listing(request):
    
    def get_date_future(future):
        now = datetime.now()
        return now + timedelta(days=future)
    
    listing_form = create_listing_form()
    categories = Categories.objects.all()
    conditions = Health.objects.all()
    all_listings = Listings.objects.all().order_by('-listing_end')
    search_form = listings_search_form()
    message = None
    
    if request.method == 'POST':
        form = create_listing_form(request.POST)
        if form.is_valid():
            #process listing form
            new_listing = Listings()
            new_listing.title = form.cleaned_data['title']
            new_listing.description = form.cleaned_data['description']
            new_listing.image_url = form.cleaned_data['image_link']
            new_listing.start_bid = form.cleaned_data['starting_bid']
            new_listing.listing_end = get_date_future(7)
            
            cat = form.cleaned_data['category']
            health = form.cleaned_data['condition']

            listing_category = Categories.objects.get(description=cat)
            listing_condition = Health.objects.get(description=health)
            listing_user_fk = User.objects.get(username = request.user)
            
            new_listing.category_fk = listing_category
            new_listing.health_fk = listing_condition
            new_listing.user_fk = listing_user_fk
            new_listing.save()            
        else:
            message = 'Form Invalid'
            return render(request, 'auctions/create_listing.html',{
                        'message': message,
                        'listing_form': listing_form,
                        'categories': categories,
                        'conditions': conditions,
            })
        
        # Listing Created Render the index Page
        message = f"Listing Created"
        return render(request, 'auctions/index.html',{
                      'message': message,
                      'listing_form': listing_form,
                      'categories': categories,
                      'conditions': conditions,
                      'listings': all_listings, 
                      'listings_search_form':search_form,
        })
    else:
        # return blank form to fill in
        return render(request, 'auctions/create_listing.html',{
                      'message': message,
                      'listing_form': listing_form,
                      'categories': categories,
                      'conditions': conditions,
        })

def add_2_watchlist(request, item_id):
    listing = Listings.objects.get(listing_id=item_id)
    
    bidform= bid_form()
    watch_message = 'Added To Watchlist'
    
    #new_watch = Watchlists(listing_fk_m2m=None, user_fk_m2m=None)
    # new_watch = Watchlists(listing_fk_m2m = listing, user_fk_m2m = the_user)

    
    # To create a Many-2-Many relationship 
    # https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_many/
    #
    # The m2m table in the logical model effectively becomes an attribute of 
    # one of the tables in the m2m relationship. 
    # 
    # In this case the watchlist is a m2m field of the User table 
    # As an item is added to the users watchlist it is added to the m2m field
    
    # To add an item to a m2m field the parent record must already exist
    # In this case the User has already been created and the watchlist attribute 
    # is being added telling us that the user is watching a Listing  
    
    current_user = User.objects.get(username=request.user)
    current_user.watchlist_m2m.add(listing)
    current_user.save()
    
    is_watched = True

    return render(request, "auctions/listing_page.html",{
                    'listing': listing,
                    'bid_form': bidform,
                    'bid_message': watch_message,
                    'is_watched': is_watched,
    })
    
def unwatch(request, item_id):
    bid_listing = Listings.objects.get(listing_id=item_id)
    current_user = User.objects.get(username = request.user)
    bidform= bid_form()
    watch_message = 'Item Removed'
    is_watched = False
    
    current_user.watchlist_m2m.remove(bid_listing)

    return render(request, "auctions/listing_page.html",{
                    'listing': bid_listing,
                    'bid_form': bidform,
                    'bid_message': watch_message,
                    'is_watched': is_watched,
    })
    
    
    
    
    
 
# In SQL with a M2M table called Watchlists between User and Listings it would be something like this
# SELECT * 
# FROM Watchlists AS W, Listings AS L
# WHERE W.listing_fk = L.listing_id AND l.is_active = True

# active_listings = Listings.objects.filter(is_active = True)

# The Django ORM allows creation of a m2m field which essentially ads this table as an attribute to one of the
# two tables in the m2m relationship along with some methods to return queries  
def load_watchlist(request):
    current_user = User.objects.get(username=request.user)
    
    if request.method=='POST':

        form = listing_auction_state_form(request.POST)
        if form.is_valid():
            state = form.cleaned_data['listing_status']
            if state == 'Active':
                watched_listings = current_user.watchlist_m2m.filter(is_active = True)
                message = 'Active Listings'
            elif state == 'Closed':
                watched_listings = current_user.watchlist_m2m.filter(is_active=False)
                message = 'Closed Listings'
            else:
                # state == 'All'
                watched_listings = current_user.watchlist_m2m.all()
                message = 'All Listings'  
        else:
            message = 'Form Validation Error'
    else:
        form = listing_auction_state_form()
        watched_listings = current_user.watchlist_m2m.all()
        message = 'All Listings' 

    return render(request, "auctions/watchlist.html",{
                    'watchlist': watched_listings,
                    'listing_states_form': form,
 
    })
                      



def index(request):
    listings = Listings.objects.filter(is_active=True).order_by('-listing_end')
    listings_search = listings_search_form()
    
    if request.method=='POST':
        # User Clicked Submit button on Search Form     

        form = listings_search_form(request.POST)
        if form.is_valid():
            category_choice = form.cleaned_data['category_choice']
            health_choice = form.cleaned_data['health_choice']
            price_choice = form.cleaned_data['price_choice']
            location_choice = form.cleaned_data['location_choice']
            print(f"Form returned Valid")
        else:
            search_form_message = "validation Error"
            category_choice = 'All'

          
        try:
            if category_choice != 'All':
                cat_choice =  Categories.objects.get(description=category_choice)
                listings = listings.filter(category_fk = cat_choice)
                print(f"##### POST ### cat_choice => {cat_choice}")
        except:
                print(f"POST category not found. assuming All => {request.POST['category_choice']}")
            
                
        try:
            if health_choice != 'All': 
                h_choice = Health.objects.get(description=health_choice)
                listings = listings.filter(health_fk = h_choice)
                print(f"##### POST ### health_choice => {h_choice}")
        except:
            print(f"POST health status not found. assuming All => {request.POST['health_choice']}")
        
        listings_search = listings_search_form(request.POST)
    else:
        print(f"### GET ###")
        
        
        
    return render(request, "auctions/index.html",{
                    'listings': listings,
                    'listings_search_form':listings_search,
    })
           
           
def end_auction(request, item_id):
    # App identifiers for message
    from_name = 'Auction-Site'
    from_email = 'auction@project2.com'
    
    # Find Auction Winner
    item = Listings.objects.get(listing_id=item_id)
    try:
        all_item_bids = Bids.objects.filter(listing_fk=item)
        highest_bid = all_item_bids.latest('bid')
        auction_winner = highest_bid.user_fk
        
        #Winners Details
        winner_name = auction_winner.username
        #winner_email = auction_winner.email
        winner_email = 'artilleryvoo@protonmail.com'
        
        # Send Winner Message
        winner_message = f"Hi {winner_name}, Congratatulations Your Bid Won!\n\nBe sure to make payment to {seller_name} without delay!"
        subject = 'You are the Highest Bidder and Won!'
        email_body = f"Name: {from_name}\nEmail: {from_email}\nMessage: {winner_message}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [winner_email]  # Replace with your desired recipient email address
        
    except:
        # No Bids, Mo Winner, Item Unsold, email failed
        pass

    
    # Sellers Details
    auction_seller = Listings.objects.get(listing_id=item_id).user_fk
    seller_name = auction_seller.username
    seller_email = auction_seller.email
    #seller_email = 'artilleryvoo@protonmail.com'
    
    #send_mail(subject, email_body, from_email, recipient_list)
    
    # Send Seller Message
    seller_message = f"Hi {seller_name}, Good News, Your Item Sold!\n\nWait until payment is made and Be sure to ship to {seller_name}!"
    subject = f"Item {item.title} Sold!"
    email_body = f"Name: {from_name}\nEmail: {from_email}\nMessage: {seller_message}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['artilleryvoo@protonmail.com']  # Replace with your desired recipient email address
    
    #send_mail(subject, email_body, from_email, recipient_list)
 
 
    # Get the User with the highest Bid
    # Send them an email with Winning Bid Payment Notice
    # Add item to Payments
    # Remove from Listings
    
    #item_id.delete()
    print(f"status => {item.is_active}")
    item.is_active = False
    item.save()
    
    
    # Render listing_page and let the user know the listing is ended
    listing_details=Listings.objects.get(listing_id = item_id)
    new_comments_form = comment_form()
        
    is_watched = check_listing_is_watched(request,item_id)
    user_is_high_bidder = check_user_is_high_bidder(request, item_id)
    comments_list = get_this_listings_comments(request,item_id)
    
    message = 'Auction Ended'

    return render(request, 'auctions/listing_page.html',{
                    'listing': listing_details,
                    'bid_message': message,
                    'is_watched': is_watched,
                    'user_is_high_bidder': user_is_high_bidder,
                    'comments_list': comments_list,
                    'comment_form': new_comments_form,
    })
  
    
                    

    





































def restart(request):
    return render(request, 'auctions/restart.html')



def pop_users():

    user_set = ['pepe', 'turkle', 'sheela', 'bowfren', 'looda', 'smol', 'sparra']    
    for name in user_set:
        try:
            User.objects.get(username=name).delete() 
        except:
            pass
        
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

def pop_health():
    Health.objects.all().delete()
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
        
def pop_categories():
    Categories.objects.all().delete()
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
        

def pop_listings():
          
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
    sheela = User.objects.get(username='sheela')
    looda = User.objects.get(username='looda')
    smol = User.objects.get(username='smol')
    sparra = User.objects.get(username='sparra') 
    
    
    timestamp_now = datetime.now 
    active_listings = [
        { 
         'title' : 'Power Beenie', 
         'description' : 'Vikings wooly hat. Warm and Ferocious', 
         'image_url' : 'https://i.imgur.com/NR6YDvM.jpeg ', 
         'start_bid' : 5.00, 
         'listing_start' : datetime(2023, 8, 9, 00, 21, 38, 486910),  
         'listing_end' : datetime(2023,8,16,00,21,38,483198), 
         'is_active': True,
         'category_fk' : cloth,
         'health_fk' : good , 
         'user_fk' : sparra 
         },
        
        { 
         'title' : 'Phaser', 
         'description' : 'Still working, but could use a new quantum disrupter module and the phase shifter is a bit wonky so best to just keep it set to Kill to be on the safe side', 
         'image_url' : 'https://i.imgur.com/MobuKql.jpeg', 
         'start_bid' : 3.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'is_active': True,
         'category_fk' : elec,
         'health_fk' : fair , 
         'user_fk' : pepe 
         },
        
        { 
         'title' : 'Weird Cat', 
         'description' : 'BioMechanical Cat Found at UFO Crash Site, seems to be trying to communicate. Nametag says Giger', 
         'image_url' : 'https://i.imgur.com/NtDE1IS.jpeg', 
         'start_bid' : 230, 
         'listing_start' : datetime(2023,8,9,8,56,3,988426), 
         'listing_end' : datetime(2023,8,16,8,56,3,984790), 
         'is_active': True,
         'category_fk' : pets, 
         'health_fk' : good , 
         'user_fk' : turkle 
         },
        
        
        {
         'title' : 'Mexican Wrestler', 
         'description' : "Vintage Mexican Wrestler **Rare**", 
         'image_url' : 'https://i.imgur.com/Y3Xihdd.jpeg', 
         'start_bid' : 1.50, 
         'listing_start' : datetime.now(), 
         'listing_end' : datetime.now() + timedelta(days=7), 
         'is_active': True,
         'category_fk' : games, 
         'health_fk' : fair, 
         'user_fk' : sheela ,
         },
        
        
        {
         'title' : 'Acoustic Guitar', 
         'description' : "Bog standard Guitar, unplayed and never been used", 
         'image_url' : 'https://i.imgur.com/FKGgNak.jpeg', 
         'start_bid' : 85, 
         'listing_start' : datetime.now(), 
         'listing_end' : datetime.now() + timedelta(days=7), 
         'is_active': True,
         'category_fk' : music, 
         'health_fk' : fair, 
         'user_fk' : sheela ,
         },      
        
        {
         'title' : 'Banjo', 
         'description' : "Excellent Condition", 
         'image_url' : 'https://i.imgur.com/ptcqrLJ.jpeg', 
         'start_bid' : 250, 
         'listing_start' : datetime.now(), 
         'listing_end' : datetime.now() + timedelta(days=7), 
         'is_active': True,
         'category_fk' : music, 
         'health_fk' : vgood, 
         'user_fk' : sheela ,
         },
                
         
        {
         'title' : 'Worn Fiddle', 
         'description' : "Many a good tune still in this old girl", 
         'image_url' : 'https://i.imgur.com/GdRAlJx.jpeg', 
         'start_bid' : 350, 
         'listing_start' : datetime.now(), 
         'listing_end' : datetime.now() + timedelta(days=7), 
         'is_active': True,
         'category_fk' : music, 
         'health_fk' : vgood, 
         'user_fk' : sheela ,
         },
                

                  
        {
         'title' : 'Watch', 
         'description' : "Genuine Digital Watch ", 
         'image_url' : ' https://i.imgur.com/3l7XaBZ.jpeg', 
         'start_bid' : 12.50, 
         'listing_start' : datetime.now(), 
         'listing_end' : datetime.now() + timedelta(days=7), 
         'is_active': True,
         'category_fk' : elec, 
         'health_fk' : mint, 
         'user_fk' : turkle ,
         },
        
        
        
                {
         'title' : 'Oil Can Guitar', 
         'description' : "Homemade Oil Can Guitar", 
         'image_url' : ' https://i.imgur.com/a3skdQa.jpg', 
         'start_bid' : 2.50, 
         'listing_start' : datetime.now(), 
         'listing_end' : datetime.now() + timedelta(days=7), 
         'is_active': True,
         'category_fk' : music, 
         'health_fk' : fair, 
         'user_fk' : turkle ,
         },
             
                
        { 
         'title' : 'Marshal Amp', 
         'description' : 'Marshal Valve Amp for Heavy Metal', 
         'image_url' : 'https://i.imgur.com/DjRlrfj.jpg', 
         'start_bid' : 30.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'is_active': True,
         'category_fk' : music,
         'health_fk' : good, 
         'user_fk' : pepe 
         },
        
        
        
        { 
         'title' : 'Baggy Trousers', 
         'description' : 'Comfy Baggy Pants for a relaxing in the house', 
         'image_url' : 'https://i.imgur.com/HMwtqkE.jpg', 
         'start_bid' : 10.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'is_active': True,
         'category_fk' : cloth,
         'health_fk' : good, 
         'user_fk' : pepe 
         },
        
        { 
         'title' : 'Harmonica', 
         'description' : 'Great for when your feelin lonesome', 
         'image_url' : 'https://i.imgur.com/eOW9siJ.jpg', 
         'start_bid' : 1.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'is_active': True,
         'category_fk' : music,
         'health_fk' : fair, 
         'user_fk' : pepe 
         },
        
        { 
         'title' : 'Chess Set', 
         'description' : 'Badass vampire chess found while exorcising a crypt of its contents ', 
         'image_url' : 'https://i.imgur.com/rOR4heC.jpg', 
         'start_bid' : 300.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'is_active': True,
         'category_fk' : games,
         'health_fk' : vgood, 
         'user_fk' : pepe 
         },
        
        { 
         'title' : 'Roller Skates', 
         'description' : 'Sadly selling as I fell over and skint my knees', 
         'image_url' : 'https://i.imgur.com/GvroFEB.jpg', 
         'start_bid' : 10.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'is_active': True,
         'category_fk' : games,
         'health_fk' : fair, 
         'user_fk' : pepe 
         },
        
        
        { 
         'title' : 'Hula Hoop', 
         'description' : 'Keep fit and Amaze people with your skills', 
         'image_url' : 'https://i.imgur.com/Gx3xqUk.jpg', 
         'start_bid' : 3.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'is_active': True,
         'category_fk' : games,
         'health_fk' : new, 
         'user_fk' : pepe 
         },
        
        { 
         'title' : 'Flea Collar', 
         'description' : 'Keeps the Fleas out', 
         'image_url' : 'https://i.imgur.com/hjN6lhX.jpg', 
         'start_bid' : 1.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'is_active': True,
         'category_fk' : pets,
         'health_fk' : vgood, 
         'user_fk' : sparra 
         },
        
        { 
         'title' : 'Dog Boots', 
         'description' : 'Highly recommend, stil months of use left in them', 
         'image_url' : 'https://i.imgur.com/YzLSuLb.jpg', 
         'start_bid' : 2.50, 
         'listing_start' : datetime(2023,8,9,0,22,54,56550), 
         'listing_end' : datetime(2023,8,16,0,22,54,53153), 
         'is_active': True,
         'category_fk' : pets,
         'health_fk' : fair, 
         'user_fk' : sparra 
         },
        
        { 
         'title' : 'Optimus Prime', 
         'description' : 'Optimus Prime with Son of Optimus Prime', 
         'image_url' : 'https://i.imgur.com/gpVzK7e.jpeg', 
         'start_bid' : 2.50, 
         'listing_start' : datetime.now(), 
         'listing_end' : datetime.now() + timedelta(days=7), 
         'is_active': True,
         'category_fk' : games,
         'health_fk' : good, 
         'user_fk' : sparra 
         },
                        
        
    ]
    
    for listing in active_listings:
        l = Listings(title = listing['title'], 
                     description = listing['description'],
                     image_url = listing['image_url'],
                     start_bid = listing['start_bid'],
                     listing_start = listing['listing_start'],
                     listing_end = listing['listing_end'],
                     is_active = listing['is_active'],      
                     category_fk = listing['category_fk'],
                     health_fk = listing['health_fk'],
                     user_fk = listing['user_fk']
                     )
        l.save() 
    
     

            
def pop_bids():
    Bids.objects.all().delete()
    # User Fkeys
    pepe = User.objects.get(username='pepe')
    turkle = User.objects.get(username='turkle')
    sheel = User.objects.get(username='sheela')
    looda = User.objects.get(username='looda')
    smol = User.objects.get(username='smol')
    sparra = User.objects.get(username='sparra') 
    
    listing_bids = [
        {   'title': 'Watch',
            'bid': 15.00,
            'bid_time': datetime.now(),
            'listing_fk': None,
            'user_fk': pepe
        },
        
        {   'title': 'Banjo',
            'bid': 275.00,
            'bid_time': datetime.now(),
            'listing_fk': None,
            'user_fk': turkle
        },
        
        {   'title': 'Phaser',
            'bid': 5.00,
            'bid_time': datetime.now(),
            'listing_fk': None,
            'user_fk': sheel
        },
        
        {   'title': 'Baggy Trousers',
            'bid': 11.00,
            'bid_time': datetime.now(),
            'listing_fk': None,
            'user_fk': sparra
        },

        {   'title': 'Hula Hoop',
            'bid': 5.00,
            'bid_time': datetime.now(),
            'listing_fk': None,
            'user_fk': turkle
        },
        
        {   'title': 'Flea Collar',
            'bid': 2.00,
            'bid_time': datetime.now(),
            'listing_fk': None,
            'user_fk': pepe
        },   
        
    ]

    for list_bid in listing_bids:
        listing = Listings.objects.get(title = list_bid['title'])
        b = Bids(
             bid = list_bid['bid'],
             listing_fk = listing,
             user_fk = list_bid['user_fk'])
        b.save()
 
def pop_comments():
 
    pepe = User.objects.get(username='pepe')
    turkle = User.objects.get(username='turkle')
    sheel = User.objects.get(username='sheela')
    looda = User.objects.get(username='looda')
    smol = User.objects.get(username='smol')
    sparra = User.objects.get(username='sparra') 
    
    test_comments = [
        {'comment':'Amazing',
         'timestamp': 'datetime.now',
         'listing_fk': None,
         'user_fk': pepe,
        },
        
        {'comment':'Super',
         'timestamp': 'datetime.now',
         'listing_fk': None,
         'user_fk': sparra,
        },
          
        {'comment':'Not for me',
         'timestamp': 'datetime.now',
         'listing_fk': None,
         'user_fk': sheel,
        },
                  
        {'comment':'Can I have one in beige?',
         'timestamp': 'datetime.now',
         'listing_fk': None,
         'user_fk': turkle,
        },      
    ]
    
    all_listings = Listings.objects.all()
    for listing in all_listings:
        for comm in test_comments:
            c = Comments(comment = comm['comment'], 
                         timestamp = comm['timestamp'], 
                         listing_fk = listing, 
                         user_fk = comm['user_fk'])
            c.save()

     
def reset(request):
  
    pop_users()
    pop_health()
    pop_categories()
    pop_listings()
    pop_bids()
    pop_comments()
        
    message='App now has Lookup Tables, Users, Listings, Bids and Comments'
    return render(request, "auctions/restart.html",{
                    'message': message
    })
    
def static_data(request):
    pop_health()
    pop_categories()
    message = 'Health and Categories Populated'
    return render(request, 'auctions/restart.html', {'message':message})

def insert_users(request):
    pop_users()
    return render(request,'auctions/restart.html', {'message':'Users Created'})
  
def insert_listings(request):
    pop_listings()    
    return render(request, 'auctions/restart.html', {'message':'Listings Populated'})
    
def insert_comments(request):
    pop_comments()
    return render(request, 'auctions/restart.html', {'message':'Comments Populated'})

def insert_bids(request):
    pop_bids()
    return render(request, 'auctions/restart.html', {'message':'Bids Populated'})
 
def delete_all(request):
    User.objects.all().delete()
    Listings.objects.all().delete()
    Categories.objects.all().delete()
    Health.objects.all().delete()
    Bids.objects.all().delete()
    Comments.objects.all().delete()
    return render(request, 'auctions/restart.html', {'message':'All Data Deleted'})

def delete_comments(request):
    Comments.objects.all().delete()
    return render(request, 'auctions/restart.html', {'message':'All Comments Deleted'}) 
 
def delete_bids(request):
    Bids.objects.all().delete()
    return render(request, 'auctions/restart.html', {'message':'All Bids Deleted'})

