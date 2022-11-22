from django.contrib import admin

from .models import AuctionListing, Bid, Comment, User

# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)