# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

#from ratings.handlers import ratings
from django.contrib.contenttypes.fields import GenericRelation

class Tweet(models.Model):
    language = models.CharField(max_length=20,null=False)
    id_str = models.CharField(max_length=50,null=False)
    source = models.TextField(default='None')
    text = models.TextField(default='None')
    created_at = models.CharField(max_length=50,null=False)
    truncated = models.BooleanField()
    coordinates = models.CharField(max_length=30,null=True)
    timestamo_ms = models.BigIntegerField()
    tweet_id = models.CharField(max_length=50,null=False)
    in_reply_to_status_id = models.TextField(default='None')
    in_reply_to_screen_name = models.TextField(default='None')
    in_reply_to_user_id = models.TextField(default=None)
    place = models.TextField(default=None)

class User(models.Model):
    follow_request_sent = models.TextField(default='None')
    geo_enabled = models.BooleanField()
    verified = models.BooleanField()
    is_translator = models.BooleanField()
    profile_use_background_image = models.BooleanField()
    profile_images_url_https = models.TextField(default='None')
    profile_sidebar_fill_color = models.TextField(default='None')
    user_id = models.CharField(max_length=50,null=False)
    followers_count = models.BigIntegerField()
    profile_text_color = models.CharField(max_length=6)
    protected = models.BooleanField()
    location = models.TextField(default='None')
    statuses_count = models.BigIntegerField()
    description = models.TextField(default='None')
    notifications = models.TextField(default='None')
    profile_background_image_url_https = models.TextField(default='None')
    profile_background_image_url = models.URLField(default='None')
    profile_background_color = models.CharField(max_length=6)
    profile_banner_url = models.URLField(default='None')
    friends_count = models.BigIntegerField()
    profile_image_url = models.URLField(default='None')
    profile_link_color = models.CharField(max_length=6)
    favourites_count = models.BigIntegerField()
    name = models.CharField(max_length=50,null=False)
    screen_name = models.CharField(max_length=50,null=False)
    url = models.URLField(max_length=50,null=False)
    created_at = models.CharField(max_length=50,null=False)
    listed_count = models.BigIntegerField()
    tweet = models.ForeignKey(Tweet,on_delete=models.CASCADE)

class RetweetedStatus(models.Model):
    text = models.TextField(default='None')
    favourite_count = models.BigIntegerField()
    source = models.TextField(default='None')
    id_str = models.CharField(max_length=50,null=False)
    retweeted = models.BooleanField()
    truncated = models.BooleanField()
    is_quote_status = models.BooleanField()
    in_reply_to_status_id = models.TextField(default='None')
    in_reply_to_screen_name = models.TextField(default='None')
    in_reply_to_user_id = models.TextField(default='None')
    retweet_count = models.BigIntegerField()
    favourited = models.BigIntegerField()
    language = models.CharField(max_length=20,null=False)
    coordinates = models.CharField(max_length=30,null=True)
    created_at = models.CharField(max_length=50,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
