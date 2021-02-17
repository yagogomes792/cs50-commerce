from django.contrib import admin
from .models import User, Auction_winner, Auction_listings, Comment, WatchList, Bid


# Register your models here.

admin.site.register(User)
admin.site.register(Auction_listings)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Auction_winner)
admin.site.register(WatchList)