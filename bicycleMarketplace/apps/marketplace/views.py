from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Bike, BotD

from datetime import datetime, timedelta

from io import BytesIO
import io
import re

import base64

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name = 'taekimm',
    api_key = '511572389411428',
    api_secret='xIYewGRpHCQQM0nF09sMC4vGJYI'
)
# Create your views here.

def home(request):
    # if user is logged in, render with context dictionary w/ userId
    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        userId = None

    bike = BotD.objects.BotD()

    context = {
        'userId': userId,
        'bike': bike
    }
    

    return render(request, 'marketplace/base_index.html', context)

def register(request):
    result = User.objects.register(request.POST)
    
    # checking if result comes back with an id (aka registration successful)
    if isinstance(result, int):
        request.session['userId'] = result
        return redirect('/browse')
    
    # unsuccessful, flash message
    else:
        for error in result:
            messages.add_message(request, messages.ERROR, error)
    return redirect(reverse('home'))

def login(request):
    try:
        result = User.objects.login(request.POST)

        #if result comes back with int, login successful
        if isinstance(result, int):
            request.session['userId'] = result
            return redirect('/browse')
        
        # unsuccessful, flash message
        else:
            for error in result:
                messages.add_message(request, messages.ERROR, error)
        return redirect(reverse('home'))

    except:
        messages.add_message(request, messages.ERROR, 'User authentication failed')
        return redirect(reverse('home'))

def logout(request):
    request.session.clear()
    return redirect(reverse('home'))

def browse(request):
    # if user is logged in, render with context dictionary w/ userId
    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        userId = None

    # logic for search
    if 'search' in request.GET:
        # regex to check if numbers only
        priceSearch_REGEX = re.compile(r'^[0-9.+_-]+$')
        if priceSearch_REGEX.match(request.GET['search']):
            # if search query is only numbers, pull by price
            bike_list = Bike.objects.filter(price__lte=request.GET['search'])

        else:
            # pull by title
            bike_list = Bike.objects.filter(title__contains=request.GET['search'])

    # logic for not search
    else:
        bike_list = Bike.objects.all()
    
    # second param num of objects per page
    paginator = Paginator(bike_list, 5)

    page = request.GET.get('page')
    bikes = paginator.get_page(page)

    context = {
        'userId': userId,
        'bikes': bikes
    }
    
    return render(request, 'marketplace/base_browse.html', context)

def bikes(request):
    # if user is logged in, render with context dictionary w/ userId
    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        userId = None

    if userId is None:
        return render(request, 'marketplace/notLoggedIn.html')
    else:
        userListings = Bike.objects.filter(seller=userId)

        context = {
            'userId': userId,
            'userListings' : userListings
        }

        return render(request, 'marketplace/base_myListings.html', context)

def viewbike(request, bikeId):
    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        userId = None

    if userId is None:
        return render(request, 'marketplace/notLoggedIn.html')
    else:
        bike = Bike.objects.get(id = bikeId)

        context = {
            'userId' : userId,
            'bike' : bike
        }

        return render(request, 'marketplace/base_viewBike.html', context)


def createbike(request):
    picture  = request.FILES['picture']
    # saving to cloudinary
    cloudinary_response = cloudinary.uploader.upload(picture)
    # peeling off url from cloudinary's response
    picture_url = cloudinary_response['url']
    # peeling off public ID from cloudinary's response
    publicId = cloudinary_response['public_id']

    # creating dictionary to pass onto models
    newBike = {
        'sellerId' : request.POST['sellerId'],
        'title' : request.POST['title'],
        'description' : request.POST['description'],
        'price' : int(request.POST['price']),
        'img' : picture_url,
        'imgId' : publicId,
        'city': request.POST['city'],
        'state' : request.POST['state']
    }
    
    # saving result into variable
    result = Bike.objects.add(newBike)

    if isinstance(result, Bike):
    # if it is an instance of a bike object, go back to page
        return redirect(reverse('bikes'))
    else:
    # else, add errors to flash messages and go back to page
        for error in result:
            messages.add_message(request, messages.ERROR.error, error)
        return redirect(reverse('bikes'))


def updatebike(request, bikeId):
    # if uploading new picture
    if 'picture' in request.FILES:
        picture  = request.FILES['picture']
        # saving to cloudinary
        cloudinary_response = cloudinary.uploader.upload(picture)
        # peeling off url from cloudinary's response
        picture_url = cloudinary_response['url']
        # peeling off public ID from cloudinary's response
        publicId = cloudinary_response['public_id']

        # creating dictionary to pass onto models
        updateBike = {
            'bikeId' : bikeId,
            'title' : request.POST['title'],
            # 'description' : request.POST.get('description', ''),
            'description' : request.POST['description'],
            'price' : int(request.POST['price']),
            'img' : picture_url,
            'imgId' : publicId,
            'city': request.POST['city'],
            'state' : request.POST['state']
        }

    else:
        updateBike = {
            'bikeId' : bikeId,
            'title' : request.POST['title'],
            'description' : request.POST['description'],
            'price' : int(request.POST['price']),
            'city': request.POST['city'],
            'state' : request.POST['state']
        }
    
    # saving result into variable
    result = Bike.objects.update(updateBike)

    if isinstance(result, int):
    # if it is an integer, go back to page
        print('hit isinstance')
        return redirect(reverse('bikes'))
    else:
    # else, add errors to flash messages and go back to page
        for error in result:
            messages.add_message(request, messages.ERROR.error, error)
        return redirect(reverse('bikes'))

def deletebike(request, bikeId):
    bike = Bike.objects.get(id=bikeId)
    bike_publicId = bike.imgId

    # deleting from cloudinary
    cloudinary.uploader.destroy(bike_publicId)
    Bike.objects.delete(bike)
    return redirect('bikes')

