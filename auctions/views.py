from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django import forms
import copy

from .models import User, Listing, Bid, Comment

# Here is the space for models forms
class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['creator', 'title', 'description', 'listing_category', 'picture_url', 'starting_bid', 'closed'] 
        # Need to add widgets to hide creator and closed and prepopulate them 
        widgets = {
            'creator' : forms.HiddenInput(),
            'closed' : forms.HiddenInput(),
        }


# end of model forms

def index(request):
    #listings_list = []
    listing = Listing.objects.all().filter(closed=False)
    return render(request, "auctions/index.html", {
        'listings' : listing,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        #l = NewListingForm(request.POST)
        #l.creator = User.objects.get(pk=request.user.id)
        form_data = copy.copy(request.POST)
        form_data['creator'] = User.objects.get(pk=request.user.id)
        form = NewListingForm(data=form_data)
        #l.cleaned_data['creator'] = User.objects.get(pk=request.user.id)
        #l.creator = User.objects.get(pk=request.user.id) 
        #obj = l.save(commit=False)
        #l.creator = request.user
        if form.is_valid():
             

            #obj = l.save(commit=False) # Return an object without saving to the DB
            #obj.creator = User.objects.get(pk=request.user.id) 
            form.save()
        # I need to populate the hidden fields
            #new_listing = l.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewListingForm()
        return render(request, "auctions/create.html", {
        "form" : form,
        #"user" : User.objects.get(pk=request.user.id) 
    })
    