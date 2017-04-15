# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Tweet, User

class TweetAdmin(admin.ModelAdmin):
    model = Tweet
    list_display = ('language', 'id_str', 'source', 'text', 'truncated', 'coordinates', 'timestamp_ms', 'in_reply_to_status_id', 'in_reply_to_screen_name', 'in_reply_to_user_id', 'place')

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('follow_request_sent', 'language', 'geo_enabled', 'verified', 'is_translator', 'profile_use_background_image', 'profile_images_url_https', 'profile_sidebar_fill_color', 'user_id', 'followers_count', 'profile_text_color', 'protected', 'location', 'statuses_count', 'description', 'notifications', 'profile_background_image_url_https', 'profile_background_image_url', 'profile_background_color', 'profile_banner_url', 'friends_count', 'profile_image_url', 'profile_link_color', 'favourites_count', 'name', 'screen_name', 'url', 'listed_count', 'tweet')

# class RetweetedStatusAdmin(admin.ModelAdmin):
#     model = RetweetedStatus
#     list_display = ('text','favourite_count', 'source', 'id_str', 'retweeted', 'truncated', 'is_quote_status', 'in_reply_to_status_id', 'in_reply_to_screen_name', 'in_reply_to_user_id', 'retweet_count', 'favourited', 'language', 'coordinates', 'created_at', 'user')

admin.site.register(Tweet, TweetAdmin)
admin.site.register(User, UserAdmin)
# admin.site.register(RetweetedStatus, RetweetedStatusAdmin)

