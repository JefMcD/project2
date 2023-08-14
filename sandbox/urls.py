from django.urls import path
from . import views

app_name='sandbox'
urlpatterns = [
    path('sql-simple-insert', views.sql_simple_insert, name='sql_simple_insert'),
    path("sql-cleanup", views.sql_cleanup, name='sql_cleanup'),
    path("sql-select-all", views.sql_select_all, name='sql_select-all'),
    path("sql-select-where", views.sql_select_where, name='sql_select-where'),
    path("sql-insert", views.sql_insert, name='sql_insert'),
    path("sql-update", views.sql_update, name='sql_update'),
    path("sql-delete", views.sql_delete, name='sql_delete'),
    path("sql-union", views.sql_union, name='sql_union'),
    path("sql-inner-join", views.sql_inner_join, name='sql_inner_join'),
    path("sql-outer-join", views.sql_outer_join, name='sql_outer_join'),
    path("sql-tuncate", views.sql_truncate, name='sql_truncate'),
    path("sql-raw", views.sql_raw, name='sql_raw'),
    
    path('fkeys', views.fkeys, name='fkeys'),
    
    path("insert-flights", views.insert_flights, name='insert_flights'),
    path("drop_airports", views.drop_airports, name='drop_airports'),
    path("drop-flights", views.drop_flights, name='drop_flights'),
    path("insert-airports", views.insert_airports, name='insert_airports'),
    path('dates', views.dates, name = 'dates'),
    path('m2m', views.m2m, name='m2m'),
    path('superuser', views.superuser, name='superuser')
]

