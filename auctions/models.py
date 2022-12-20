from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    categoryName = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.categoryName}"

class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, blank=True, null= True, on_delete=models.CASCADE, related_name="category")
    imageUrl = models.CharField(max_length=5000)
    startPrice = models.FloatField()
    currentPrice = models.FloatField(null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    stillActive = models.BooleanField(default=True)
    seller = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="user")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"
    
# class Bid(models.Model):
#     bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidded")
#     product = models.ManyToManyField(Listing, related_name="biddings")
#     bid = models.IntegerField()

#     def __str__(self):
#         return f"{self.bidder} {self.product.title} {self.bid}"

# class Comment(models.Model):
#     pass