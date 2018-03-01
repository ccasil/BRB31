from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^welcome$', views.welcome),
	url(r'^favorites$', views.favorites),
	url(r'^logout$', views.logout)
]