# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
from models import User, Tweet
from django.db import transaction
import ast
from django.http import JsonResponse
import math

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
                print e[1]
                uncount+=1
                print "Unable to commit////////" + str(uncount)
            minibatch_tweet = []
            minibatch_user = []

def location_view(request):
    COUNTRIES = {
        "AF": ("Afghanistan"),
        "AX": ("Aland Islands"),
        "AL": ("Albania"),
        "DZ": ("Algeria"),
        "AS": ("American Samoa"),
        "AD": ("Andorra"),
        "AO": ("Angola"),
        "AI": ("Anguilla"),
        "AQ": ("Antarctica"),
        "AG": ("Antigua and Barbuda"),
        "AR": ("Argentina"),
        "AM": ("Armenia"),
        "AW": ("Aruba"),
        "AU": ("Australia"),
        "AT": ("Austria"),
        "AZ": ("Azerbaijan"),
        "BS": ("Bahamas"),
        "BH": ("Bahrain"),
        "BD": ("Bangladesh"),
        "BB": ("Barbados"),
        "BY": ("Belarus"),
        "BE": ("Belgium"),
        "BZ": ("Belize"),
        "BJ": ("Benin"),
        "BM": ("Bermuda"),
        "BT": ("Bhutan"),
        "BO": ("Bolivia (Plurinational State of)"),
        "BQ": ("Bonaire, Sint Eustatius and Saba"),
        "BA": ("Bosnia and Herzegovina"),
        "BW": ("Botswana"),
        "BV": ("Bouvet Island"),
        "BR": ("Brazil"),
        "IO": ("British Indian Ocean Territory"),
        "BN": ("Brunei Darussalam"),
        "BG": ("Bulgaria"),
        "BF": ("Burkina Faso"),
        "BI": ("Burundi"),
        "CV": ("Cabo Verde"),
        "KH": ("Cambodia"),
        "CM": ("Cameroon"),
        "CA": ("Canada"),
        "KY": ("Cayman Islands"),
        "CF": ("Central African Republic"),
        "TD": ("Chad"),
        "CL": ("Chile"),
        "CN": ("China"),
        "CX": ("Christmas Island"),
        "CC": ("Cocos (Keeling) Islands"),
        "CO": ("Colombia"),
        "KM": ("Comoros"),
        "CD": ("Congo (the Democratic Republic of the)"),
        "CG": ("Congo"),
        "CK": ("Cook Islands"),
        "CR": ("Costa Rica"),
        "CI": ("Cote d'Ivoire"),
        "HR": ("Croatia"),
        "CU": ("Cuba"),
        "CW": ("Curacao"),
        "CY": ("Cyprus"),
        "CZ": ("Czechia"),
        "DK": ("Denmark"),
        "DJ": ("Djibouti"),
        "DM": ("Dominica"),
        "DO": ("Dominican Republic"),
        "EC": ("Ecuador"),
        "EG": ("Egypt"),
        "SV": ("El Salvador"),
        "GQ": ("Equatorial Guinea"),
        "ER": ("Eritrea"),
        "EE": ("Estonia"),
        "ET": ("Ethiopia"),
        "FK": ("Falkland Islands  [Malvinas]"),
        "FO": ("Faroe Islands"),
        "FJ": ("Fiji"),
        "FI": ("Finland"),
        "FR": ("France"),
        "GF": ("French Guiana"),
        "PF": ("French Polynesia"),
        "TF": ("French Southern Territories"),
        "GA": ("Gabon"),
        "GM": ("Gambia"),
        "GE": ("Georgia"),
        "DE": ("Germany"),
        "GH": ("Ghana"),
        "GI": ("Gibraltar"),
        "GR": ("Greece"),
        "GL": ("Greenland"),
        "GD": ("Grenada"),
        "GP": ("Guadeloupe"),
        "GU": ("Guam"),
        "GT": ("Guatemala"),
        "GG": ("Guernsey"),
        "GN": ("Guinea"),
        "GW": ("Guinea-Bissau"),
        "GY": ("Guyana"),
        "HT": ("Haiti"),
        "HM": ("Heard Island and McDonald Islands"),
        "VA": ("Holy See"),
        "HN": ("Honduras"),
        "HK": ("Hong Kong"),
        "HU": ("Hungary"),
        "IS": ("Iceland"),
        "IN": ("India"),
        "ID": ("Indonesia"),
        "IR": ("Iran (Islamic Republic of)"),
        "IQ": ("Iraq"),
        "IE": ("Ireland"),
        "IM": ("Isle of Man"),
        "IL": ("Israel"),
        "IT": ("Italy"),
        "JM": ("Jamaica"),
        "JP": ("Japan"),
        "JE": ("Jersey"),
        "JO": ("Jordan"),
        "KZ": ("Kazakhstan"),
        "KE": ("Kenya"),
        "KI": ("Kiribati"),
        "KP": ("Korea (the Democratic People's Republic of)"),
        "KR": ("Korea (the Republic of)"),
        "KW": ("Kuwait"),
        "KG": ("Kyrgyzstan"),
        "LA": ("Lao People's Democratic Republic"),
        "LV": ("Latvia"),
        "LB": ("Lebanon"),
        "LS": ("Lesotho"),
        "LR": ("Liberia"),
        "LY": ("Libya"),
        "LI": ("Liechtenstein"),
        "LT": ("Lithuania"),
        "LU": ("Luxembourg"),
        "MO": ("Macao"),
        "MK": ("Macedonia (the former Yugoslav Republic of)"),
        "MG": ("Madagascar"),
        "MW": ("Malawi"),
        "MY": ("Malaysia"),
        "MV": ("Maldives"),
        "ML": ("Mali"),
        "MT": ("Malta"),
        "MH": ("Marshall Islands"),
        "MQ": ("Martinique"),
        "MR": ("Mauritania"),
        "MU": ("Mauritius"),
        "YT": ("Mayotte"),
        "MX": ("Mexico"),
        "FM": ("Micronesia (Federated States of)"),
        "MD": ("Moldova (the Republic of)"),
        "MC": ("Monaco"),
        "MN": ("Mongolia"),
        "ME": ("Montenegro"),
        "MS": ("Montserrat"),
        "MA": ("Morocco"),
        "MZ": ("Mozambique"),
        "MM": ("Myanmar"),
        "NA": ("Namibia"),
        "NR": ("Nauru"),
        "NP": ("Nepal"),
        "NL": ("Netherlands"),
        "NC": ("New Caledonia"),
        "NZ": ("New Zealand"),
        "NI": ("Nicaragua"),
        "NE": ("Niger"),
        "NG": ("Nigeria"),
        "NU": ("Niue"),
        "NF": ("Norfolk Island"),
        "MP": ("Northern Mariana Islands"),
        "NO": ("Norway"),
        "OM": ("Oman"),
        "PK": ("Pakistan"),
        "PW": ("Palau"),
        "PS": ("Palestine, State of"),
        "PA": ("Panama"),
        "PG": ("Papua New Guinea"),
        "PY": ("Paraguay"),
        "PE": ("Peru"),
        "PH": ("Philippines"),
        "PN": ("Pitcairn"),
        "PL": ("Poland"),
        "PT": ("Portugal"),
        "PR": ("Puerto Rico"),
        "QA": ("Qatar"),
        "RE": ("Reunion"),
        "RO": ("Romania"),
        "RU": ("Russian Federation"),
        "RW": ("Rwanda"),
        "BL": ("Saint Barthelemy"),
        "SH": ("Saint Helena, Ascension and Tristan da Cunha"),
        "KN": ("Saint Kitts and Nevis"),
        "LC": ("Saint Lucia"),
        "MF": ("Saint Martin (French part)"),
        "PM": ("Saint Pierre and Miquelon"),
        "VC": ("Saint Vincent and the Grenadines"),
        "WS": ("Samoa"),
        "SM": ("San Marino"),
        "ST": ("Sao Tome and Principe"),
        "SA": ("Saudi Arabia"),
        "SN": ("Senegal"),
        "RS": ("Serbia"),
        "SC": ("Seychelles"),
        "SL": ("Sierra Leone"),
        "SG": ("Singapore"),
        "SX": ("Sint Maarten (Dutch part)"),
        "SK": ("Slovakia"),
        "SI": ("Slovenia"),
        "SB": ("Solomon Islands"),
        "SO": ("Somalia"),
        "ZA": ("South Africa"),
        "GS": ("South Georgia and the South Sandwich Islands"),
        "SS": ("South Sudan"),
        "ES": ("Spain"),
        "LK": ("Sri Lanka"),
        "SD": ("Sudan"),
        "SR": ("Suriname"),
        "SJ": ("Svalbard and Jan Mayen"),
        "SZ": ("Swaziland"),
        "SE": ("Sweden"),
        "CH": ("Switzerland"),
        "SY": ("Syrian Arab Republic"),
        "TW": ("Taiwan (Province of China)"),
        "TJ": ("Tajikistan"),
        "TZ": ("Tanzania, United Republic of"),
        "TH": ("Thailand"),
        "TL": ("Timor-Leste"),
        "TG": ("Togo"),
        "TK": ("Tokelau"),
        "TO": ("Tonga"),
        "TT": ("Trinidad and Tobago"),
        "TN": ("Tunisia"),
        "TR": ("Turkey"),
        "TM": ("Turkmenistan"),
        "TC": ("Turks and Caicos Islands"),
        "TV": ("Tuvalu"),
        "UG": ("Uganda"),
        "UA": ("Ukraine"),
        "AE": ("United Arab Emirates"),
        "GB": ("United Kingdom of Great Britain and Northern Ireland"),
        "UM": ("United States Minor Outlying Islands"),
        "US": ("United States of America"),
        "UY": ("Uruguay"),
        "UZ": ("Uzbekistan"),
        "VU": ("Vanuatu"),
        "VE": ("Venezuela (Bolivarian Republic of)"),
        "VN": ("Viet Nam"),
        "VG": ("Virgin Islands (British)"),
        "VI": ("Virgin Islands (U.S.)"),
        "WF": ("Wallis and Futuna"),
        "EH": ("Western Sahara"),
        "YE": ("Yemen"),
        "ZM": ("Zambia"),
        "ZW": ("Zimbabwe"),
    }
    country_count = {}
    places = Tweet.objects.values('place')
    for location in places:
        if location['place'] is not None and location['place'] != "null":
            place = location['place']
            place = ast.literal_eval(place)
            country_count[place['country_code']] = country_count.get(place['country_code'], 0) + 1

    country_name_count = {COUNTRIES[k]:math.log(v) for k, v in country_count.items()}

    #print country_name_count
    return JsonResponse(country_name_count)

def index(request):
    return render(request,'home.html')


def apphome(request):
    return render(request,'apphome.html')

def contact(request):
    return render(request,'contact.html')

def langpop(request):
    return render(request,'language_compare.html')

def wordpop(request):
    return render(request,'word_compare.html')
