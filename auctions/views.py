from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .forms import *
from .models import *


def index(request):
    listings = Listing.objects.all()
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

# Allow signed-in users to create a new auctionlisting
@login_required(login_url="login")
def create(request):
    if request.method == "POST":
        form = CreateListing(request.POST, request.FILES)
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


def list_view(request, list_url):
    # Get the auction listing
    list_title = list_url.replace("_", " ")
    auction = Listing.objects.get(title=list_title)

    # Check user is logged in
    if request.user.is_authenticated:
        # Get user's object
        user = User.objects.get(username=request.user.username)
        # Get all the people watching the auction
        observers = auction.observing.all()
        
        # Iterate over all the observers
        for observer in observers:

            # Check if this user is part of the observers for this auction
            if observer.username == user:
                return render(request, "auctions/listing.html", {
                    'listing': auction,
                    'message': "Remove from Watchlist"
                })

        # Display add to watchlist
        return render(request, "auctions/listing.html", {
                    'listing': auction,
                })

    return render(request, "auctions/listing.html", {
        'listing': auction
        })

@login_required
def watchlist(request):
    if request.method == "POST":
        if request.user.username == request.POST.get("username"):
            username = request.user.username
            product = request.POST.get("product")

            # Get the complete data sumbitted via post from the database
            user_instance = User.objects.get(username=username)
            user_id = user_instance.id
            list_instance = Listing.objects.get(title=product)

            # Remove  product from watchlist
            if request.POST.get("command") == "Remove from Watchlist":
                watchlist = Watchlist.objects.get(username=user_id)
                watchlist.product.remove(list_instance)
                return HttpResponseRedirect(reverse("index"))

            # Add product to watchlist
            try:
                watchlists = Watchlist.objects.get(username=user_id)
                watchlist_products = watchlists.product.all()
                if watchlist_products.exists():
                    for watchlist in watchlist_products:
                        # Check if the new watchlist is already in the user's watchlist
                        if watchlist.title == product:
                            # Redirect them to the index page
                            return HttpResponseRedirect(reverse("index"))
                        else:
                            # Add watchlist
                            watchlists.product.add(list_instance)
                            # Redirect them to the index page
                            return HttpResponseRedirect(reverse("index"))
                else:
                    watchlists.product.add(list_instance)
                    return HttpResponseRedirect(reverse("index"))
            except ObjectDoesNotExist:
                # Create new watchlist with this username
                new_watchlist = Watchlist(username=user_instance)
                new_watchlist.save()
                new_watchlist.product.add(list_instance)
                return HttpResponseRedirect(reverse("index"))
            
        else:
            return HttpResponseRedirect(reverse("index"))
