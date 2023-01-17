from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import CreateListing, CommentForm, BidForm
from .models import Bid, Category, Comment, Listing, User


def index(request):
    activeListings = Listing.objects.all()
    for listing in activeListings:
        currentBid = Bid.objects.filter(product=listing).last()
        if currentBid:
            listing.currentPrice =  currentBid.bid
        else:
            listing.currentPrice = listing.startPrice
        listing.save()
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
    currentBid = Bid.objects.filter(product=listing).last()
    if currentBid:
        listing.currentPrice =  currentBid.bid
    else:
        listing.currentPrice = listing.startPrice
    listing.save()
    inWatchlist = user in listing.watchers.all()
    comments= Comment.objects.filter(listing=listing)
    context = {
        'listing':listing,
        'inWatchlist':inWatchlist,
        'comments':comments,
        'commentForm':CommentForm(),
        'bidForm':BidForm()
    }
    return render(request, "auctions/listing.html", context)

def displayWatchlist(request):
    user = request.user
    userWatchlists = user.watchlist.all()
    context = {'watchlists': userWatchlists}
    return render(request, "auctions/watchlist.html", context)

def addOrRemoveWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    if user in listing.watchers.all():
        listing.watchers.remove(user)
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        listing.watchers.add(user)
        return HttpResponseRedirect(reverse("watchlist"))

def addComment(request, id):
    user = request.user
    listing = Listing.objects.get(pk=id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.writer = user
        comment.listing = listing
        comment.save()
        return HttpResponseRedirect(reverse("listings", kwargs={'id':listing.id}))


def add_bid(request, id):
    # Get data from the form
    newBid = float(request.POST['bid'])
    listing = Listing.objects.get(pk=id)
    if newBid > listing.currentPrice:
        listing.currentPrice = newBid
        listing.save()
        form = BidForm(request.POST)
        newBid = form.save(commit=False)
        newBid.product = listing
        newBid.bidder = request.user
        newBid.save()
        messages.success(request, "Your bid has been accepted")
        return HttpResponseRedirect(reverse("listings", kwargs={'id':listing.id}))
    else:
        messages.error(request, "Your bid is lower than the current bid")
        return HttpResponseRedirect(reverse("listings", kwargs={'id':listing.id}))

def closeListing(request, id):
    listing = Listing.objects.get(pk=id)
    listing.stillActive=False
    # Get buyer's name from bid
    buyer = Bid.objects.filter(product=listing).last().bidder
    listing.buyer = buyer
    listing.save()
    messages.success(request, "Auction successfully closed")
    return HttpResponseRedirect(reverse("index"))