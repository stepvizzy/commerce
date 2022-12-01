from django.contrib import admin

from .models import *
from .forms import *

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'auctioneer']

class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ('product',)

admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(User)