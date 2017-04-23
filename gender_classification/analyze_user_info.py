# -*- coding: utf-8 -*-
"""
    anaylze_user_info.py
    Use bio, reputation, nickname: obtain valuable data?
"""
from util import parser


class Analyzer:

    def __init__(self):
        self.cities = parser.read_cities()

    def eval_username(self, user_json, male_names, female_names):

        return 0


    def eval_location(self, user_json):

        possible_locs = []

        bio = user_json["bio"]

        for word in bio.split():
            if word in self.cities:
                possible_locs.append(word)

        return possible_locs



    def eval_age(self, user_json, min_age, max_age):
        #max_age = 26
        #min_age = 16

        bio = user_json["bio"]
        possible_age = [int(s) for s in bio.split() if s.isdigit()]

        if len(possible_age):
            for num in possible_age:
                if min_age <= num <= max_age:
                    return num
