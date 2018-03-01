# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
	return render(request, 'br/index.html')

def register(request):
	if request.method == 'POST':
		password = request.POST['password']
		cpassword = request.POST['cpassword']
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
	return render(request, 'br/welcome.html')

def favorites(request):
	return render(request, 'br/favorites.html')

def logout(request):
	request.session.clear()
	return redirect('/')