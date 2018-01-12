from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import User, Bike

from io import BytesIO
import io

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
        context = {
            'userId': userId
        }
        return render(request, 'marketplace/index.html', context)
    # else render w/o context dictionary
    else:
        return render(request, 'marketplace/index.html')

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
    
    context = {
        'userId': userId,
        'results': []
    }
    return render(request, 'marketplace/browse.html', context)


def bikes(request):
    # if user is logged in, render with context dictionary w/ userId
    if 'userId' in request.session:
        userId = request.session['userId']
    else:
        userId = None

    context = {
        'userId': userId,
        'userListings': [
            {
                'title': 'test',
                'description': 'test description',
                'price': 100,
                'city': 'Los Angeles',
                'state': 'CA'
            },
            {
                'title': 'test2',
                'description': 'test description2',
                'price': 200,
                'city': 'LA',
                'state': 'CA'
            }    
        ]
    }

    if userId is None:
        return render(request, 'marketplace/notLoggedIn.html')
    else:
        return render(request, 'marketplace/listings.html', context)

def createbike(request):
    #print(request.POST)
    #print(request.FILES['picture'])
    picture  = request.FILES['picture']

    cloudinary_response = cloudinary.uploader.upload(picture)
    picture_url = cloudinary_response['url']

def updatebike(request):
    pass

def deletebike(request):
    pass
