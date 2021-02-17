from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction_listings(models.Model):
    owner = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    first_bid = models.IntegerField()
    category = models.CharField(max_length=100)
    image = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name}"


class Bid(models.Model):
    user = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bid = models.FloatField()
    auction_listing_id = models.IntegerField()

    def __str__(self):
        return f"{self.user} {self.title}"


class Comment(models.Model):
    user = models.CharField(max_length=100)
    comment = models.TextField(max_length=200)
    comment_timestamp = models.DateTimeField(auto_now_add=True)
    auction_listing_id = models.IntegerField()


class WatchList(models.Model):
    user = models.CharField(max_length=100)
    auction_listing_id = models.IntegerField()


class Auction_winner(models.Model):
    owner = models.CharField(max_length=100)
    winner = models.CharField(max_length=100)
    winnerPrice = models.FloatField()
    title = models.CharField(max_length=100)
    auction_listing_id = models.IntegerField()

