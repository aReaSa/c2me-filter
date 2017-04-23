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

    username = "XXXXXXXXXXXXX"
    password = "XXXXXXXXXXXXX"
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

