# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

#from ratings.handlers import ratings
from django.contrib.contenttypes.fields import GenericRelation

class Tweet(models.Model):
    language = models.CharField(max_length=20,null=False)
    retweet_count = models.BigAutoField()
    favorited = models.BigAutoField()
    id_str = models.CharField(max_length=50,null=False)

class RetweetedStatus(models.Model):
    text = models.TextField(default='None')
    tweet = model.ForeignKey(Tweet,on_delete=models.CASCADE)
    favourite_count = models.BigAutoField()
    source = models.TextField(default='None')
    retweeted = models.BooleanField()
    truncated = models.BooleanField()
    is_quote_status = models.BooleanField()
    in_reply_to_status_id = models.TextField(default='None')
    coordinates = models.CharField(max_length=30,null=True)
    user = model.ForeignKey(User,on_delete=models.CASCADE)

class User(models.Model):
    geo_enabled = models.BooleanField()
    verified = models.BooleanField()
    is_translator = models.BooleanField()
    profile_use_background_image = models.BooleanField()
    profile_images_url_https = models.TextField(default='None')
    profile_sidebar_fill_color = models.TextField(default='None')
    user_id = models.CharField(max_length=50,null=False)
    followers_count = models.BigAutoField()
    profile_text_color = models.CharField(max_length=6)
    protected = models.BooleanField()
    location = models.TextField(default='None')
    statuses_count = models.BigAutoField()
    description = models.TextField(default='None')
    friends_count = models.BigAutoField()
    profile_image_url = models.TextField(default='None')
    profile_link_color = models.CharField(max_length=6)
    favourites_count = models.BigAutoField()
    name = models.CharField(max_length=50,null=False)
    url = models.CharField(max_length=50,null=False)
    created_at = models.CharField(max_length=50,null=False)
    listed_count = models.BigAutoField()
    tweet = model.ForeignKey(Tweet,on_delete=models.CASCADE)
    
    
    

   
