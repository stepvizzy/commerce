from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(blank=True, max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media/images')
    starting_bid = models.IntegerField()
    auctioneer = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name="auctions")

    def __str__(self):
        return f"{self.title}"
    
    def title_to_url(self):
        return self.title.replace(' ', '_')

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidded")
    product = models.ManyToManyField(Listing, related_name="biddings")
    bid = models.IntegerField()

class Comment(models.Model):
    pass

class Watchlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="observer")
    product = models.ManyToManyField(Listing, blank=True, related_name="observing")

    def __str__(self):
        return f"{self.id}: {self.username}"