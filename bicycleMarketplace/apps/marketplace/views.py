# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
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
    print request.POST
    # print request.FILES['picture']
    picture  = request.FILES['picture']

    with open(picture, 'rb') as image_file:
        # encoded_string = base64.b64encode(image_file.read())
        # cloudinary_response = cloudinary.uploader.upload(encoded_string)
        # print cloudinary_response

        cloudinary_response = cloudinary.uploader.upload(image_file.read())

    
    # with picture.open('rb') as image_file:
    #     encoded_string = base64.b64encode(image_file.read())

    # encoded_string = base64.b64encode(request.FILES['picture'].read())

    
    

    # image_read = picture.read()
    # image_64_encode = base64.encodestring(image_read)
    # # image_64_decode = base64.decodestring(image_64_encode)
    # # image_result = open(request.FILES['picture'], 'wb')

    # picture = BytesIO(image_64_encode)
    # cloudinary.uploader.upload(picture)
    
        
    # picture = BytesIO(request.FILES['picture'].read())
    # print 'PASSED BytesIO'
    
    # result = cloudinary.uploader.upload(picture)
    # print 'PASSED UPLOAD'
    # print result



def updatebike(request):
    pass

def deletebike(request):
    pass
