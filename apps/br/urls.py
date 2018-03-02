from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^welcome$', views.welcome),
	url(r'^favorites$', views.favorites),
	url(r'^flavors$', views.flavors),
	url(r'^display/(?P<id>\d+)$', views.display),
	url(r'^addtofavorites/(?P<id>\d+)$', views.addtofavorites),
	url(r'^removefromfavorites/(?P<id>\d+)$', views.removefromfavorites),
	url(r'^logout$', views.logout)
]