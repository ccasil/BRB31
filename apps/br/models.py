from __future__ import unicode_literals
from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['password']) < 1 or len(postData['cpassword']) < 1 or len(postData['birthday']) < 1:
			errors['field'] = "Make sure all fields are filled"
		if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
			errors['names'] = "Make sure first name and last name are at least 2 characters long"
		if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
			errors['namenum'] = "Name must not contain any numbers!"
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "Invalid Email address"
		if len(postData['password']) < 8 or len(postData['cpassword']) < 8:
			errors['password'] = "Password must be at least 8 characters long"
		if postData['password'] != postData['cpassword']:
			errors['confirm'] = "Make sure passwords match"
		if len(errors) == 0:
			hashpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
		 	userreg = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], birthday=postData['birthday'], password=hashpw)
			errors['userreg'] = userreg
		return errors
	def login_validator(self, postData):
		errors = {}
		checkemail = User.objects.filter(email=postData['email'])
		if checkemail:
			if bcrypt.checkpw(postData['password'].encode(), checkemail[0].password.encode()):
				errors['userlog'] = checkemail[0]
			else:
				errors['invalidpass'] = "Invalid Password or Email"
		else:
			errors['invalidemail'] = "Invalid Email or Password"
		return errors

class User(models.Model):
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	birthday = models.DateTimeField()
	password = models.CharField(max_length = 255)
	objects = UserManager()

class IceCream(models.Model):
	flavor = models.CharField(max_length = 255)
	imgname = models.CharField(max_length = 255, default="")
	description = models.TextField()
	users = models.ManyToManyField(User, related_name="items")

class Ranking(models.Model):
	rank = models.IntegerField()
	favoriter = models.ForeignKey(User, related_name="favorites")
	favorited = models.ForeignKey(IceCream, related_name="favorites")