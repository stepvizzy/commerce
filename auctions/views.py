from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import AuctionListing, Bid, Comment, User

class CreateListing(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = '__all__'
        exclude = ('auctioneer',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Title','class':'form-control'}),
            'category': forms.TextInput(attrs={'placeholder': 'Category', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'placeholder': 'Description', 'class': 'form-control'}),
            'bid': forms.NumberInput(attrs={'class':'form-control', 'style':'width: 500px;'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }

def index(request):
    listings = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        form = CreateListing(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            # save aucitonlisting to db
            instance = form.save(commit=False)
            instance.auctioneer = request.user
            instance.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render (request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": CreateListing()
    })