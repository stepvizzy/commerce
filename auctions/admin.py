from django.contrib import admin

from .models import Bid, Category, Comment, Listing, User

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'startPrice', 'currentPrice']
    filter_horizontal = ('watchers',)

# class WatchlistAdmin(admin.ModelAdmin):
#     filter_horizontal = ('product',)

admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)


"""
admin.site.register(Bid)

admin.site.register(Watchlist, WatchlistAdmin)
"""