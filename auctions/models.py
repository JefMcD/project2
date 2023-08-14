from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import tzinfo, timedelta, datetime, timezone

#######################################################################
#
#   Primary-Keys
#
#   If No Primary Key is defined for a Model
#   Django Handles The Database Tables Primary Keys
#   and automatically creates a Primary Key 
#   called 'id' which is of Type BigAutoField.
#
#   This can be defined either in settings.py
#   DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#
#   or in apps.py
#   class AuctionsConfig(AppConfig):
#       default_auto_field = 'django.db.models.BigAutoField'
#       name = 'auctions'
#
#   Foriegn Keys
#   on-delete refers to the other table. ie what to do when the record that is being referenced is deleted
#
#
#   Migrations
#
#   To create initial migrations for an app, run makemigrations and specify the app name. 
#   The migrations folder will be created.
#   ./manage.py makemigrations <myapp>
#   ie
#   $ python3 manage.py makemigrations auctions
#   $ python3 manage.py migrate
#   
#
#
#   Migrations Errors
#
#   This error occured and I dont understand it
#   django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency
#
#   Solution
#   Delete all of your migrations ??? (How do you delete migrations) or Drop the Database (delete db.sqlite3) and rerun the migrations
#   https://stackoverflow.com/questions/44651760/django-db-migrations-exceptions-inconsistentmigrationhistory
#
######################################################################




class Listings(models.Model):
    listing_id      = models.AutoField(primary_key=True,
                                          db_index=True)
    title           = models.CharField(max_length=20)
    description     = models.CharField(max_length=255)
    image_url       = models.CharField(max_length=255, default='https://i.imgur.com/e02INp6.png')
    start_bid       = models.FloatField(default=1)
    listing_start   = models.DateTimeField(auto_now_add=True)
    listing_end     = models.DateTimeField()
    is_active       = models.BooleanField(default=True)
    
    category_fk     = models.ForeignKey('Categories',
                                        on_delete=models.CASCADE)
    health_fk       = models.ForeignKey('Health',
                                        on_delete=models.CASCADE)
    user_fk         = models.ForeignKey('User',
                                        on_delete = models.CASCADE)
    

    
    def highest_bid(self):
        all_bids = Bids.objects.filter(listing_fk=self.pk)
        if not all_bids:
            # no bids
            hibid = 0.00
        else:
            hibid = all_bids.latest('bid').bid
        return hibid
    
    def __str__(self):
        return f"{self.title} : {self.description} : {self.start_bid} : {self.start_bid} : {self.listing_start} : {self.listing_end} : {self.category_fk}"
    
    
    
class Categories(models.Model):
    category_id     = models.AutoField(primary_key=True,
                                          db_index=True)
    description     = models.CharField(max_length=45)
    
    def __str__(self):
        return f"{self.category_id} : {self.description}"
    
class Health(models.Model):
    health_id       = models.AutoField(primary_key=True,
                                          db_index=True)
    description     = models.CharField(max_length=45)
    
    def __str__(self):
        return f"{self.health_id}: {self.description}"
    
    
    
class Bids(models.Model):
    bid_id          = models.AutoField(primary_key=True,
                                          db_index=True)
    bid             = models.FloatField(default=1.00)
    bid_time        = models.DateTimeField(auto_now=True)
    listing_fk      = models.ForeignKey('Listings',
                                        on_delete=models.CASCADE)
    user_fk         = models.ForeignKey('User',
                                        on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.bid_id}, {self.bid}: {self.bid_time}: {self.listing_fk}: {self.user_fk}"
    
class Comments(models.Model):
    comment_id      = models.AutoField(primary_key=True, 
                                          db_index=True)
    comment         = models.CharField(max_length=255)
    timestamp       = models.DateTimeField(auto_now=True)
    listing_fk      = models.ForeignKey('Listings',
                                        on_delete=models.CASCADE)
    user_fk         = models.ForeignKey('User',
                                        on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.comment}, {self.listing_fk}, {self.user_fk}"
    
class Watchlists_basic(models.Model):
    listing_fk      = models.ForeignKey('Listings',
                                        on_delete=models.CASCADE)
    user_fk         = models.ForeignKey('User',
                                        on_delete=models.CASCADE,
                                        db_index=True)
    
class User(AbstractUser):
    watchlist_m2m = models.ManyToManyField(Listings, related_name='unused')








#############################################################################   
#    
# Example Tables From CS50Lecture and tutorials for sandbox
#
#############################################################################
class Airports(models.Model):
    # default primary key is id of type BigAutoField
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)
    def __str__(self):
        return (f"\n{self.id}: {self.code}: {self.city}\n")
    
#class Flights(models.Model):
    # default primary key is id of type BigAutoField
	#origin = models.ForeignKey(Airports, on_delete=models.CASCADE, related_name='departures')
	#destination = models.ForeignKey(Airports, on_delete=models.CASCADE, related_name='arrivals')
	#duration = models.IntegerField()
 
    
    
class Flights(models.Model):
    # default primary key is id of type BigAutoField
    origin = models.ForeignKey(Airports, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Airports, on_delete=models.CASCADE, related_name='arrivals')
    duration = models.IntegerField()
    
    def __str__(self):
        return(f"{self.id}: {self.origin} to {self.destination}")  
    
    
    
    
    
  
class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ["headline"]

    def __str__(self):
        return self.headline
    
    
    
    
 







    
    
    
    
     
     
     
     