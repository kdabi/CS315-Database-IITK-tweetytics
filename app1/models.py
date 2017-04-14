# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

#from ratings.handlers import ratings
from django.contrib.contenttypes.fields import GenericRelation

class Tweet(models.Model):
    language = models.CharField(max_length=20,null=True)
    id_str = models.CharField(max_length=50, primary_key=True)
    source = models.TextField(default='None',null=True)
    text = models.TextField(default='None',null=True)
    truncated = models.NullBooleanField(null=True)
    coordinates = models.CharField(max_length=150,null=True)
    timestamp_ms = models.BigIntegerField(null=True)
    # tweet_id = models.CharField(max_length=50,null=True)
    in_reply_to_status_id = models.TextField(default='None',null=True)
    in_reply_to_screen_name = models.TextField(default='None',null=True)
    in_reply_to_user_id = models.TextField(default=None,null=True)
    place = models.TextField(default=None,null=True)

class User(models.Model):
    follow_request_sent = models.TextField(default='None',null=True)
    geo_enabled = models.NullBooleanField(null=True)
    verified = models.NullBooleanField(null=True)
    is_translator = models.NullBooleanField(null=True)
    profile_use_background_image = models.NullBooleanField(null=True)
    profile_images_url_https = models.TextField(default='None',null=True)
    profile_sidebar_fill_color = models.TextField(default='None',null=True)
    user_id = models.CharField(max_length=50,null=False)
    followers_count = models.BigIntegerField(null=True)
    profile_text_color = models.CharField(max_length=6,null=True)
    protected = models.NullBooleanField(null=True)
    location = models.TextField(default='None',null=True)
    statuses_count = models.BigIntegerField(null=True)
    description = models.TextField(default='None',null=True)
    notifications = models.TextField(default='None',null=True)
    profile_background_image_url_https = models.TextField(default='None',null=True)
    profile_background_image_url = models.URLField(max_length=150,default='None',null=True)
    profile_background_color = models.CharField(max_length=6,null=True)
    profile_banner_url = models.URLField(max_length=150,default='None',null=True)
    friends_count = models.BigIntegerField(null=True)
    profile_image_url = models.URLField(max_length=150,default='None',null=True)
    profile_link_color = models.CharField(max_length=6,null=True)
    favourites_count = models.BigIntegerField(null=True)
    name = models.CharField(max_length=50,null=True,default=None)
    screen_name = models.CharField(max_length=50,null=True)
    url = models.URLField(max_length=150,null=True)
    #created_at = models.CharField(max_length=50,null=True)
    listed_count = models.BigIntegerField(null=True)
    tweet = models.ForeignKey(Tweet,on_delete=models.CASCADE)

# class RetweetedStatus(models.Model):
#     text = models.TextField(default='None')
#     favourite_count = models.BigIntegerField()
#     source = models.TextField(default='None')
#     id_str = models.CharField(max_length=50,null=False)
#     retweeted = models.NullBooleanField()
#     truncated = models.NullBooleanField()
#     is_quote_status = models.NullBooleanField()
#     in_reply_to_status_id = models.TextField(default='None')
#     in_reply_to_screen_name = models.TextField(default='None')
#     in_reply_to_user_id = models.TextField(default='None')
#     retweet_count = models.BigIntegerField()
#     favourited = models.BigIntegerField()
#     language = models.CharField(max_length=20,null=False)
#     coordinates = models.CharField(max_length=30,null=True)
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
