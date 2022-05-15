from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=140)
    picture_url = models.URLField()
    starting_bid = models.FloatField(default=0) # added a default zero value because this field was added later.
    closed = models.BooleanField(default=False)

    # Need to add the list of categories to choose from:
    FASHION = 'FA'
    SPORT = 'SP'
    MUSIC = 'MU'
    FURNITURE = 'FU'
    ART = 'AR'
    OTHER = 'OT'
    CATEGORY_CHOICES = [
        (FASHION, 'Fashion'),
        (SPORT, 'Sport'),
        (MUSIC, 'Music'),
        (FURNITURE, 'Furniture'),
        (ART, 'Art'),
        (OTHER, 'Other'),
    ]
    listing_category = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=OTHER,
    )
    
class Bid(models.Model):
    bid_price = models.FloatField()
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.CharField(max_length=400)
    commented_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
      
    