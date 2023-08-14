from django.urls import path

from . import views
app_name='auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('restart', views.restart, name='restart'),
    path('reset', views.reset, name='reset'),
    path('static_data', views.static_data, name='static_data'),
    path('insert_users', views.insert_users, name='insert_users'),
    path('insert_listings', views.insert_listings, name='insert_listings'),
    path('insert_bids', views.insert_bids, name='insert_bids'),   
    path('insert_comments', views.insert_comments, name='insert_comments'),
    
    path('delete_all', views.delete_all, name='delete_all'),
    path('delete_bids', views.delete_bids, name='delete_bids'),
    path('delete_comments', views.delete_comments, name='delete_comments'),
    
    path("register", views.register, name="register"),


    path('create_listing', views.create_listing, name='create_listing'),
    path('listing_page/<int:listing_pkey>', views.listing_page, name='listing_page'),
    
    path('process_bid/<int:bid_listing_id>', views.process_bid, name='process_bid'),

    path('add_2_watchlist<int:item_id>', views.add_2_watchlist, name='add_2_watchlist'),
    path('unwatch<int:item_id>', views.unwatch, name='unwatch'),
    path('load_watchlist', views.load_watchlist, name='load_watchlist'),
    
    path('end_auction/<int:item_id>', views.end_auction, name='end_auction'),
    
    path('process_comment/<int:listing_pkey>', views.process_comment, name='process_comment'),
    
]
