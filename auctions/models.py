from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(blank=True, max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, upload_to='media/images')
    starting_bid = models.IntegerField()
    auctioneer = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="auctions")

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidded")
    auction = models.ManyToManyField(AuctionListing, related_name="biddings")
    bid = models.IntegerField()

class Comment(models.Model):
    pass