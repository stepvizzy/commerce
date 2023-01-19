from django.contrib import admin
from django import forms
from .models import Bid, Category, Comment, Listing, User
from .forms import BidFormAdmin
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'startPrice', 'currentPrice']
    filter_horizontal = ('watchers',)

class BidAdmin(admin.ModelAdmin):
    form = BidFormAdmin
    list_display = ['bidder', 'product', 'bid']

admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid, BidAdmin)