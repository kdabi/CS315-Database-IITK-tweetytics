# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
from models import User, Tweet
from django.db import transaction

# Create your views here.
def load_data(filename):
    with open(filename) as data_file:
        data = json.loads(data_file.read())

    count = 1
    uncount = 0
    fields = [
        #'created_at',
        #'entities',
        'id',
        'in_reply_to_screen_name',
        'in_reply_to_status_id',
        'in_reply_to_user_id',
        'lang',
        'place',
        #'possibly_sensitive',
        #'quoted_status_id or quoted_status_id_str',
        #'quoted_status',
        #'retweeted_status',
        'source',
        'text',
        'truncated',
        'user',
        'coordinates',
        'timestamp_ms',
        #'display_text_range',
        #'extended_entities',
        #'extended_tweet',
    ]

    user_fields = [
        'follow_request_sent',
        'geo_enabled',
        'verified',
        'is_translator',
        'profile_use_background_image',
        'profile_images_url_https',
        'profile_sidebar_fill_color',
        'id',
        'lang',
        'followers_count',
        'profile_text_color',
        'protected',
        'location',
        'statuses_count',
        'description',
        'notifications',
        'profile_background_image_url_https',
        'profile_background_image_url',
        'profile_background_color',
        'profile_banner_url',
        'friends_count',
        'profile_image_url',
        'profile_link_color',
        'favourites_count',
        'name',
        'screen_name',
        'url',
        'created_at',
        'listed_count',
    ]
    minibatch_tweet=[]
    minibatch_user=[]
    for post1 in data:
        post = {}
        for field in fields:
            try:
                if type(post1[field]) is str:
                    try:
                        post1[field].decode('utf-8')
                        post[field] = post1[field]
                    except UnicodeError:
                        post[field] = None
                else:
                    post[field] = post1[field]
            except KeyError:
                post[field] = None
        # print field, post['coordinates']

        user1 = {}

        for field in user_fields:
            try:
                if type(post['user'][field]) is str:
                    try:
                        post['user'][field].decode('utf-8')
                        user1[field] = post['user'][field]
                    except UnicodeError:
                        user1[field] = None
                else:
                    user1[field] = post['user'][field]

            except KeyError:
                user1[field] = None
            #print field, user1[field]

        try:
            # minibatch_tweet.append(Tweet(
            #     id_str = str(post['id']),
            #     in_reply_to_screen_name = post['in_reply_to_screen_name'],
            #     in_reply_to_status_id = str(post['in_reply_to_status_id']),
            #     in_reply_to_user_id = str(post['in_reply_to_user_id']),
            #     language = post['lang'],
            #     place = post['place'],
            #     #possibly_sensitive = post['possibly_sensitive'],
            #     #quoted_status_id = post['quoted_status_id'],
            #     #quoted_status = post['quoted_status'],
            #     #retweeted_status = post['retweeted_status'],
            #     source = post['source'],
            #     text = post['text'],
            #     truncated = post['truncated'],
            #     #user = post['user'],
            #     coordinates = post['coordinates'],
            #     timestamp_ms = post['timestamp_ms'],
            #     #display_text_range = post['display_text_range'],
            #     #extended_entities = post['extended_entities'],
            #     #extended_tweet = post['extended_tweet'],
            #     tweet_id = post['id'] ))

            new_tweet = Tweet(
                #created_at = post['created_at'],
                #entities = post['entities'],
                id_str = str(post['id']),
                in_reply_to_screen_name = post['in_reply_to_screen_name'],
                in_reply_to_status_id = str(post['in_reply_to_status_id']),
                in_reply_to_user_id = str(post['in_reply_to_user_id']),
                language = post['lang'],
                place = json.dumps(post['place']),
                #possibly_sensitive = post['possibly_sensitive'],
                #quoted_status_id = post['quoted_status_id'],
                #quoted_status = post['quoted_status'],
                #retweeted_status = post['retweeted_status'],
                source = post['source'],
                text = post['text'],
                truncated = post['truncated'],
                #user = post['user'],
                coordinates = post['coordinates'],
                timestamp_ms = post['timestamp_ms'],
                #display_text_range = post['display_text_range'],
                #extended_entities = post['extended_entities'],
                #extended_tweet = post['extended_tweet'],
                # tweet_id = post['id']
            )
            minibatch_tweet.append(new_tweet)
            new_user = User(
                follow_request_sent= user1['follow_request_sent'],
                geo_enabled = user1['geo_enabled'],
                verified = user1['verified'],
                is_translator = user1['is_translator'],
                profile_use_background_image = user1['profile_use_background_image'],
                profile_images_url_https = user1['profile_images_url_https'],
                profile_sidebar_fill_color = user1['profile_sidebar_fill_color'],
                user_id = user1['id'],
                language = user1['lang'],
                followers_count = user1['followers_count'],
                profile_text_color = user1['profile_text_color'],
                protected = user1['protected'],
                location = user1['location'],
                statuses_count = user1['statuses_count'],
                description = user1['description'],
                notifications = user1['notifications'],
                profile_background_image_url_https = user1['profile_background_image_url_https'],
                profile_background_image_url = user1['profile_background_image_url'],
                profile_background_color = user1['profile_background_color'],
                profile_banner_url = user1['profile_banner_url'],
                friends_count = user1['friends_count'],
                profile_image_url = user1['profile_image_url'],
                profile_link_color = user1['profile_link_color'],
                favourites_count = user1['favourites_count'],
                name = user1['name'],
                screen_name = user1['screen_name'],
                url = user1['url'],
                #created_at = user1['created_at'],
                listed_count = user1['listed_count'],
                tweet = new_tweet
            )
            minibatch_user.append(new_user)
        except Exception as e:
            print e
            print "Unable to create instance"

        if len(minibatch_tweet)==100:
            try:
                with transaction.atomic():
                    out = Tweet.objects.bulk_create(minibatch_tweet)
                    # for index, val in enumerate(out):
                    #     print val.id
                    User.objects.bulk_create(minibatch_user)
                print "created" + str(count)
                count+=1
            except Exception as e:
                print e
                uncount+=1
                print "Unable to commit////////" + str(uncount)
            minibatch_tweet = []
            minibatch_user = []

def location_view(request):
    pass

def index(request):
    return render(request,'home.html')


def apphome(request):
    return render(request,'apphome.html')

def contact(request):
    return render(request,'contact.html')

def wordpop(request):
    return render(request,'word_compare.html')
