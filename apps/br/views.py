# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from datetime import date, time, datetime, timedelta
# from time import gmtime, strftime
import bcrypt

def index(request):
	return render(request, 'br/index.html')

def register(request):
	if request.method == 'POST':
		# password = request.POST['password']
		# cpassword = request.POST['cpassword']
		errors = User.objects.basic_validator(request.POST)
		if 'userreg' in errors:
			request.session['id'] = errors['userreg'].id
		 	request.session['record'] = "registered!"
			return redirect('/welcome')
		else:
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
			return redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.login_validator(request.POST)
		if 'userlog' in errors:
			request.session['id'] = errors['userlog'].id
			return redirect('/welcome')
		else:
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
	return redirect('/')

def welcome(request):
	today = date.today()
	january = date(today.year, 1, 31)
	march = date(today.year, 3, 31)
	may = date(today.year, 5, 31)
	july = date(today.year, 7, 31)
	august = date(today.year, 8, 31)
	october = date(today.year, 10, 31)
	december = date(today.year, 12, 31)
	data = {
		"time": "There are %d days until the next 31st of the month!" % ((july - today).days)
		# http://strftime.org/
		# https: // www.guru99.com/date-time-and-datetime-classes-in-python.html
	}
	return render(request, 'br/welcome.html', data)

def favorites(request):
	#rankorder = Ranking.objects.order_by('ranking')
	data = {
		'flavors': IceCream.objects.filter(users=request.session['id']),
		'ranking': Ranking.objects.filter(favoriter_id=request.session['id'])
	}
	return render(request, 'br/favorites.html', data)

def flavors(request):
	data = {
		'flavors': IceCream.objects.all()
	}
	return render(request, 'br/flavors.html', data)

def addtofavorites(request, id):
	icecream = IceCream.objects.get(id=id)
	user = User.objects.get(id=request.session['id'])
	user.items.add(icecream)
	Ranking.objects.create(rank=31, favorited_id=id, favoriter_id=request.session['id'])
	return redirect('/favorites')

def removefromfavorites(request,id):
	user = User.objects.get(id=request.session['id'])
	ice = IceCream.objects.get(id=id)
	user.items.remove(ice)
	return redirect('/favorites')

def display(request,id):
	data = {
		'flavors': IceCream.objects.get(id=id),
		# 'ranking': Ranking.objects.get(favoriter_id=request.session['id'])
	}
	return render(request, 'br/display.html', data)

def logout(request):
	request.session.clear()
	return redirect('/')
