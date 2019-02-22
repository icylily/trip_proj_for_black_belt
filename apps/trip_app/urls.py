from django.conf.urls import url, include
from . import views
# from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^trip_create$', views.process_create_trip),
    url(r'^process/add_trip$',views.process_add),
    url(r'^process/edit_a_trip$', views.process_edit),
    url(r'^(?P<trip_id>\d+)$', views.process_detail),
    url(r'^edit/(?P<trip_id>\d+)$', views.edit),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete_a_trip),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^deletejoin/(?P<trip_id>\d+)$', views.delete_a_join),
]
