# -*- coding: utf-8 -*-
import tensorflow as tf
from bs4 import BeautifulSoup
import re
import urllib
from urllib.request import urlopen
from urllib.request import Request
import zlib
import json
import numpy as np
import sys
import cv2
import locale
import time
"""
File: parser.py
    from connected2.me
    Retrieve user photos and meta-data and store it for gender detection algorithm.
"""

CITIES_FILE_PATH = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/resources/cities.txt"


def shuffle(username, password):

    """
        No need for username and password, cookie in the header works fine for now.
        @:return: bytes: json containing user data
    """

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive',
           'Referer': 'https://connected2.me'}
           # 'Cookie': '__ar_v4=U6JOPOWOX5GIVEHHWHSJUB%3A20160610%3A25%7CRC72UI2K2FDMJK4OSE4MVG%3A20160610%3A25%7CLK5BNWSXERCA3FCEOUZUWV%3A20160610%3A25; __utma=159415471.1811788850.1460895125.1473540752.1476722619.8; __utmc=159415471; __utmz=159415471.1460930134.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); mp_2cd419a2654f2f82e2b6aa382f6d0190_mixpanel=%7B%22distinct_id%22%3A%20%2215614ffade53b4-0d4d1424a6745a-3f65450b-1fa400-15614ffade642e%22%2C%22%24initial_referrer%22%3A%20%22http%3A%2F%2Fconnected2.me%2Fmain%22%2C%22%24initial_referring_domain%22%3A%20%22connected2.me%22%7D; optimizelyEndUserId=oeu1486148355078r0.1498210284817938; deviceID=jpBuPp2ND1yX1jAxYW4PIIlqM8HtQX5T; showStatusTip=true; homeSignupLayout=default; __cfduid=d90878c4f68d40d679aee91405b7410791490000954; user_attributes="{\"device_id\":\"224c792fc7f182f423a1ec368d251e92\"}"; mp_05babb024dc6a4d104e9781eb06a8ef1_mixpanel=%7B%22distinct_id%22%3A%20%22komputersayntist%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%7D; mp_mixpanel__c=20; optimizelySegments=%7B%225690621952%22%3A%22direct%22%2C%225696671078%22%3A%22false%22%2C%225673901742%22%3A%22gc%22%7D; optimizelyBuckets=%7B%7D; userNick="2|1:0|10:1491611812|8:userNick|24:a29tcHV0ZXJzYXludGlzdA==|981c02556d6be59b708f37d5f4aa28fa1d2f014d26941b83cec1a79687a8002f"; anonPassword="2|1:0|10:1491611812|12:anonPassword|56:RDFGZGRNQTdqTzlKV3o5UWdKYllIeFpIbEVQWjJHUUcwbG83am5KOQ==|50757adaf3b848d41bd75f3039cdda8996ca67a488717c101981ea4b00c78170"; userPassword="2|1:0|10:1491611812|12:userPassword|12:bTNobTN0NGwx|69fdce51e6eecce161fba30cc95c25af7ab240ed3176c5a3a0fd0619bba176a8"; anonNick="2|1:0|10:1491611812|8:anonNick|28:YW5vbi02MWEzNTc2MzJjMDc5MWQ=|436375855ccffbcc31b8ffac07f84780cc9e5ae8e25d26e1c73d736c7b2ab5d0"; _gat_UA-25377145-1=1; _ga=GA1.2.1811788850.1460895125; _gat_UA-25377145-10=1'}

    shuffle_req_url = "https://api.connected2.me/b/shuffle?nick=" + username + "&password=" + password
    req = Request(shuffle_req_url, headers=hdr)

    try:
        response = urlopen(req)
    except:
        print("Can't open url")

    encoding = response.info().get_content_charset('utf8')
    decompressed_data = zlib.decompress(response.read(), 15+32)
    decompressed_data = remove_emoticons(decompressed_data)
    user_json = json.loads(decompressed_data.decode(encoding))

    return user_json


def search_shuffle(key):

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive',
           'Referer': 'https://connected2.me'}

    millis = int(round(time.time() * 1000))
    shuffle_req_url = "https://api.connected2.me/b/search?s=" + key + "&_=" + str(millis)
    req = Request(shuffle_req_url, headers=hdr)

    try:
        response = urlopen(req)
    except:
        print("Can't open url")

    encoding = response.info().get_content_charset('utf8')
    decompressed_data = zlib.decompress(response.read(), 15+32)
    #decompressed_data = remove_non_emoticons(decompressed_data)
    user_json = json.loads(decompressed_data.decode(encoding))

    return user_json


def filter_shuffle():

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive',
           'Referer': 'https://connected2.me'}

    username = "bigblackhole"
    password = "3215987a"
    age_start = 21
    age_stop = 23
    distance = 50
    gender = "f"
    order = 1

    filter_uri = "http://api.connected2.me/b/shuffle_filter" + "?age_start=" + str(age_start) + "&age_stop=" + str(age_stop)
    filter_uri += "&gender=" + gender #+ "&distance=" + str(distance)  # "&order_by_last_online=" + str(order)
    filter_uri += "&nick=" + username + "&password=" + password

    filter = "https://api.connected2.me/b/receipt_android"
    # TODO: HANDLE DISTANCE

    # lat = "39.874615"
    # lon = "32.747596"
    # info_uri = "https://api.connected2.me/b/g_info" + "?nick=" + username + "&password=" + password + "&lat=" + lat + "&lon=" + lon
    #
    # SHUFFLE_LOCATION_KEY = "shuffle_location_key";
    # LOCATION_LAT_KEY = "location_lat_key";
    # LOCATION_LON_KEY = "location_lon_key";
    #
    # req = Request(filter_uri, headers=hdr)
    #
    # try:
    #     response = urlopen(req)
    # except:
    #     return "LOL"
    #
    # encoding = response.info().get_content_charset('utf8')
    # decompressed_data = zlib.decompress(response.read(), 15+32)
    # #decompressed_data = remove_emoticons(decompressed_data)
    # user_json = json.loads(decompressed_data.decode(encoding))
    #
    # return user_json

    ############################
    req = Request(filter_uri, headers=hdr)

    try:
        response = urlopen(req)
    except:
        return "LOL"

    encoding = response.info().get_content_charset('utf8')
    decompressed_data = zlib.decompress(response.read(), 15+32)
    #decompressed_data = remove_emoticons(decompressed_data)
    user_json = json.loads(decompressed_data.decode(encoding))

    return user_json




def retrieve_profile_picture(pp_link):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive',
           'Referer': 'https://connected2.me'}

    req = Request(pp_link, headers=hdr)

    try:
        response = urlopen(req)
    except urllib.request.HTTPError as e:
        if e.code == 404:
            print("Can't open image link")
            return None

    # convert byte array to numpy
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    #cv2.imshow("image", image)
    #cv2.waitKey(0)

    return image



def remove_emoticons(text):
    return ''.join([i if ord(i) < 352 else ' ' for i in text])


# Return list of cities
def read_cities(city_file_path):

    f = open(city_file_path, "r")
    cities = [s.lower() for s in f.read().split() if s.isalpha()]
    return cities

