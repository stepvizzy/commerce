from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .forms import CreateListing
from .models import Category, Listing, User


def index(request):
    activeListings = Listing.objects.filter(stillActive=True)
    context = {'activeListings' : activeListings}
    return render(request, "auctions/index.html", context)

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

# Create a new listing for the user 
@login_required(login_url="login")
def createListing(request):
    # If user visit page via post method
    if request.method == "POST":
        # Populate form with data from post request
        form = CreateListing(request.POST)
        if form.is_valid():
            # save listing to db
            newListing = form.save(commit=False)
            newListing.seller = request.user
            newListing.currentPrice = request.POST.get('startPrice')
            newListing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render (request, "auctions/create.html", {
                "form": CreateListing()
            })

    # If user visit page via get method display the form
    context = {"form": CreateListing()}
    return render(request, "auctions/create.html", context)

def displayCategories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, "auctions/category.html", context)

def selectedCategoryListing(request, category):
    category = Category.objects.get(categoryName=category).id
    activeListing = Listing.objects.filter(stillActive=True, category=category)
    context = {'activeListings': activeListing}
    return render(request, "auctions/index.html", context)


def listing(request, id):
    # Get the auction listing
    user = request.user
    listing = Listing.objects.get(pk=id)
    inWatchlist = user in listing.watchers.all()

    context = {'listing':Listing.objects.get(pk=id), 'inWatchlist':inWatchlist}
    return render(request, "auctions/listing.html", context)

def addWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchers.add(user)
    return HttpResponseRedirect(reverse("listings", kwargs={'id':listing.id}))

def removeWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchers.remove(user)
    return HttpResponseRedirect(reverse("listings", kwargs={'id':listing.id}))

def displayWatchlist(request):
    user = request.user
    userWatchlists = user.watchlist.all()
    context = {'watchlists': userWatchlists}
    return render(request, "auctions/watchlist.html", context)

# def add_bid(request):
#     if request.method == "POST":
#         current_bid = int(request.POST.get("bid"))
#         product_instance = Listing.objects.get(title=request.POST.get("product"))
#         user_instance = User.objects.get(username=request.user.username)
        
#         try:
#             bids = Bid.objects.get(product=product_instance).bid
#             user_id = user_instance.id
#             if current_bid > max(bids):
#                 new_bid = Bid(bidder=user_id)
#                 new_bid.save()

#         except ObjectDoesNotExist:
#             if current_bid > product_instance.starting_bid:
#                 new_bid = Bid(bidder=user_instance, product=product_instance, bid=current_bid)
#                 return HttpResponseRedirect(reverse("index"), {
#                     'bid_message':'bid placed successfully'
#                 })