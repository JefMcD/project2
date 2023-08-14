from django.shortcuts import render
from auctions.models import Health, Categories
from auctions.models import *
# Create your views here.


def fkeys (request):

    
    all_listings = Listings.objects.all()
    
    bid_listing_id = 3
    bid_listing = Listings.objects.get(listing_id=bid_listing_id)
    
    all_bids = Bids.objects.all()
    
    
    # What are all bids for listing 2
    
    # Bids has a fk - listings_fk
    # So find the listing object for listing 2
    
    q_listing = Listings.objects.get(listing_id = 2)
    
    # SELECT * FROM BIDS WHERE listing_fk = 2
    # SELECT * FROM Bids WHERE listing_fk =  q_listing
    all_bids_for_l2 = Bids.objects.filter(listing_fk = q_listing)
    high_bid = all_bids_for_l2.latest('bid').bid
    
    
    return render(request, 'sandbox/dates.html', {
                    'all_listings': all_listings,
                    'bid_listing': bid_listing,
                    'l2_bids': all_bids_for_l2,
                    'high_bid': high_bid

    })



# SELECT *.* FROM Categories
def sql_select_all(request):
    all_categories = Categories.objects.all()    
    return render(request, 'auctions/index.html')



# SELECT * FROM Airports WHERE city='New York'
def sql_select_where(request):
    
    # If there is likely to be more than one record
    airport = Airports.objects.filter(city='New York')

    # or return the first if more than one returned
    first_airport = Airports.objects.filter(city='New York').first()

    # If there you know there is only one tuple, get returns only one
    only_airport = Airports.objects.get(city='New York')
        
    return render(request, 'auctions/index.html')



# Select First record in a Table
# SELECT * FROM Categories LIMIT 1;
def sql_select_first(request):
    first_category = Categories.objects.first()
    # or
    all_categories = Categories.objects.all()
    first = all_categories.first()
    
    # attributes can them be accessed thisly
    cat_id = first.category_id
    cat_desc = first.description
        
    return render(request, 'auctions/index.html')




# Simple INSERT into Table with No FKey and PKey health_id an AutoField and one other field called 'description'
# mysql> INSERT INTO Health (description) VALUES ('broken')

def sql_simple_insert(request):
    new_health = Health(description = 'broken')
    new_health.save()
    
    return render(request, 'auctions/index.html')





# INSERT INTO Flights (origin, destination, duration)
#        VALUES (2,1,415)
#
# attribites with values 2 and 1 being foreign keys values
#
def sql_insert(request):
    # get foreign key for origin attribute
    jfk = Airports.objects.get(city='New York')

    #get foreign key for destination attribute
    cdg = Airports.objects.get(city='Paris')
    
    # Insert statement
    new_flight = Flights(origin=jfk, destination=cdg, duration=415)
    new_flight.save()
    




# UPDATE Airports SET city='Glezga' WHERE city='Glasgow'    
def sql_update(request):
    g = Airports.objects.get(city='Glasgow')
    g.city='Glezga'
    g.save()

# Delete first record in a table
def sql_delete(request):
    defunct = Categories.objects.first()
    defunct.delete()

def sql_union(request):
    pass

def sql_union(request):
    pass

def sql_inner_join(request):
    pass

def sql_outer_join(request):
    pass

# basic    # mysql> DELETE FROM Listings WHERE listing_id = 2;
# standard # mysql> DELETE FROM Listings WHERE listing_id = 1 AND title = 'comfy jumper'
# with FK  # mysql> DELETE FROM Listings WHERE title='honker' AND category='Musical Instruments'
def sql_delete(request):
    remove_listings = Listings.objects.get(title='Rubbish Listing')
    for rubbish in remove_listings:
        rubbish.delete()


def sql_truncate(request):
    pass

# mysql> DELETE ALL FROM Listings;
def sql_cleanup(request):
    listings = Listings.objects.all()
    for listing in listings:
        listing.delete()



def sql_raw(request):
    pass


def insert_flights(request):
    # this is written long-hand just to be super specific about whats happening
    # equivalent to
    # SELECT * FROM Airports WHERE code = 'JFK'
    # Note that inside brackets '=' is acting as equivalence and not assignment here
    jfk = Airports.objects.get(code = 'JFK')
    lhr = Airports.objects.get(code = 'LHR')
    cdg = Airports.objects.get(code = 'CDG')
    gla = Airports.objects.get(code = 'GLA')
    bar = Airports.objects.get(code = 'BAR')
    
    f1 = Flights(origin=jfk, destination=lhr, duration=455)
    f1.save()
    
    f2 = Flights(origin=cdg, destination=gla, duration=90)
    f2.save
    
    f3 = Flights(origin=gla, destination=bar, duration=90)
    f3.save()
    
    
    # origin and destination are each a ForiegnKey to Airports
    # In Flights, They need to be assigned to the entire tuple/record in the Airports Table
    # You cant just assign them the value of the Primary Key you want. 
    # That Dont work and will give an error.
    
    return render(request, 'auctions/index.html')

def insert_airports(request):
    airports = [
        {'code':'LHR', 'city':'London'},
        {'code':'CDG', 'city':'Paris'},
        {'code':'JFK', 'city':'New York'},
        {'code':'GLA', 'city':'Glasgow'},
        {'code':'BAR', 'city':'Barcelona'},
    ]
    for airport in airports:
        print (f"code: {airport['code']} ")
        a = Airports(code=airport['code'], city=airport['city'])
        a.save()
    # a = Airports(code='LAX', city='Los Angeles')
    # a.save()
    return render(request, 'auctions/index.html')
        
def drop_airports(request):
    airports = Airports.objects.all()
    for airport in airports:
        airport.delete()
        
    return render(request, 'auctions/index.html')

def drop_flights(request):
    flights = Flights.objects.all()
    for flight in flights:
        flight.delete()
        
    return render(request, 'auctions/index.html')


def dates(request):
    def get_date_future(future):
        now = datetime.now()
        return now + timedelta(days=future)

    date_now = datetime.now()
    date_future = get_date_future(7)
    return render(request, 'sandbox/dates.html',{
                    'date_now': date_now,
                    'date_future': date_future
    })
    
    
def m2m(request):
    Publication.objects.all().delete()
    p1 = Publication(title="The Python Journal")
    p1.save()
    p2 = Publication(title="Science News")
    p2.save()
    p3 = Publication(title="Science Weekly")
    p3.save()
    
    publications = Publication.objects.all()
    
    # Create an Article
    a1 = Article(headline="Django lets you build web apps easily")
    a1.save()
    
    # Add a Publication it is published(p1) in to the m2m field(publications)
    a1.publications.add(p1)
    
    # Adding a duplicate will be ignored
    a1.publications.add(p1)
    
    # Create another Article
    a2 = Article(headline="NASA uses Python")
    a2.save()
    
    # Add more publications that the article appears in to the m2m field(publications)
    a2.publications.add(p1, p2)
    a2.publications.add(p3)
    
    publications = a1.publications.all()
    
    
    
    
    return render(request, 'sandbox/dates.html', {
                    'publications':publications
    })
    
    
def superuser(request):
    try:
        user = User.objects.get(username = 'chief')
        admin_message = 'username = chief found'
    except:
        admin_message = 'username = chief exception'

    return render(request, 'sandbox/dates.html', {
                    'admin_message': admin_message
    })
    

