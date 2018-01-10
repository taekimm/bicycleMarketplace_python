# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import re, bcrypt, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    # register function
    def register(self, data):
        # empty array to hold all errors from validation
        errors = []
        
        # check on fname alphabet only
        if not data['fname'].isalpha():
            errors.append('First name may only contain letters')
            
        # check on first name length
        if len(data['fname']) < 1:
            errors.append('First name must be longer than 1 character')
            
        # check on last name alphabets only
        if not data['lname'].isalpha():
            errors.append('Last name may only contain letters')
		
		# check on last name length
        if len(data['lname']) < 1:
            errors.append('Last name must be longer than 1 character')
        
        # check if email is input
        if len(data['email']) < 1:
            errors.append('Email required')
            
        # email format check
        if not EMAIL_REGEX.match(data['email']):
            errors.append('Email must be in valid format')
        
        # password length check
        if len(data['password']) < 8:
            errors.append('Password must be 8 characters or longer')
        
        # password & password confirm check
        if data['password'] != data['password_confirm']:
            errors.append('Passwords must match') 
            
        # checking if passed error checks
        if len(errors) == 0:
            # using get to see if there are multiple users with said email
            # if .get() errors out, user with that email already exists.
			try:
				User.objects.get(email=data['email'])
				errors.append('User with that email already exists')
				return errors
			except: 
				user = User.objects.create(fname=data['fname'], lname=data['lname'], email=data['email'], password=bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()))
				return user.id
        else:
			return errors

    # login function
    def login(self, data):
		errors = []

		# checking if email is input
		if len(data['email']) < 1:
			errors.append('Email required')

		# checking email format w/ regex
		if not EMAIL_REGEX.match(data['email']):
			errors.append('Email must be in valid format')

		# checking length of password
		if len(data['password']) < 8:
			errors.append('Password must be 8 characters or longer')

		# if no errors appened
		if len(errors) == 0:
			# try to get THE user - if the user does not exist, go to except
			try:
				user = User.objects.get(email__iexact=data['email'])
				encrypted_pw = bcrypt.hashpw(data['password'].encode(), user.password.encode())
				if encrypted_pw == user.password.encode():
					return user.id
			except: 
				errors.append('User authentication failed')
				return errors
		else:
			return errors

class User(models.Model):
	def __unicode__(self):
		return self.fname + " " + self.lname
	
	fname = models.CharField(max_length = 255)
	lname = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	# to use UserManager
	objects = UserManager()

class BikeManager(models.Manager):
    def add(self, data):
        errors = []
        seller = User.objects.get(id=data['userId'])

        # checks on Bike inputs
        if len(data['title']) < 0:
            errors.append('Please enter a name of your bike')
        
        if len(data['description']) < 0:
            errors.append('Please enter a description of your bike')
        
        if len(data['img']) < 0:
            errors.append('Please attach an image of your bike')
        
        if data['price'] < 0:
            errors.append('Please enter a price for your bike')

        if len(data['city']) < 0:
            errors.append('Please enter a city')

        if len(data['state']) < 0:
            errors.append('Please enter a state')

class Bike(models.Model):
    def __unicode__(self):
        return str(self.title) + ' sold by: ' + str(self.seller)

    title = models.CharField(max_length = 255)
    description = models.TextField()
    img = models.CharField(max_length = 255)
    price = models.IntegerField()
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 255)
    seller = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # to use BikeManager
    objects = BikeManager()


