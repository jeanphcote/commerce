from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=140)
    picture_url = models.URLField()
    closed = models.BooleanField(default=False)

class Bid(models.Model):
    bid_price = models.FloatField()
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
