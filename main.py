# -*- coding: utf-8 -*-
from util import parser
from gender_classification.analyze_user_info import Analyzer
from util import train_samples
from gender_classification import face_detector
import glob
import ast
import cv2
import os
from resources.urls import *


def user_read_from_file():

    analyzer = Analyzer()
    for file in glob.glob(HAS_FACE_PATH + "*.txt"):
        f = open(file, "r", encoding="utf8", errors="ignore")

        # preprocess json remove emoticons etc.
        user_text = parser.remove_emoticons(f.read())
        user_json = ast.literal_eval(user_text)

        possible_age = analyzer.eval_age(user_json)
        possible_loc = analyzer.eval_location(user_json)

        print("------" + user_json["nick"] + "---------")
        #print(user_json["bio"])
        print(possible_age)
        print(possible_loc)
        f.close()
    return


def obtain_samples():
    MAX_ITER = 1000

    has_face_path = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/filtered_shuffle/has_face/"
    image_faces_path = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/filtered_shuffle/has_face/face_images/"

    non_face_path = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/filtered_shuffle/non_face/"
    image_non_faces_path = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/filtered_shuffle/non_face/non_face_images/"

    user_set = set()

    for i in range(0, MAX_ITER):

        user_json = parser.filter_shuffle()
        print("# of users for this shuffle: " + str(len(user_json["online_users"])))
        for i in range(0, len(user_json["online_users"])):
            nickname = user_json["online_users"][i]["nick"]

            # if user in the set, don't include it again
            if nickname not in user_set:

                user_set.add(nickname)
                low_res_url = user_json["online_users"][i]["images"]["low_res"]  # may contain 72x72 images, changing...
                hi_res_url = user_json["online_users"][i]["images"]["hi_res"]

                # broken link, continue

                image = parser.retrieve_profile_picture(hi_res_url)

                if image is None:
                    continue

                height, width, channels = image.shape

                # To detect face, image size must be at least 200x200
                if height > 300 and width > 300:

                    res_image = cv2.resize(image, (300, 300), fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  # resize image to 200x200

                    if face_detector.detect(res_image):
                        user_json["online_users"][i]["has_face"] = 1
                        f = open(has_face_path + nickname + '.txt', "w+", encoding="utf-8")
                        f.write(str(user_json["online_users"][i]))
                        f.close()
                        cv2.imwrite(image_faces_path + nickname + ".jpg", res_image)

                    else:
                        user_json["online_users"][i]["has_face"] = 0
                        f = open(non_face_path + nickname + '.txt', "w+", encoding="utf-8")
                        f.write(str(user_json["online_users"][i]))
                        f.close()

                        cv2.imwrite(image_non_faces_path + nickname + ".jpg", res_image)

                else:
                    print("Image size is too small, cannot detect face")
    return None


def main():

    obtain_samples()
    return

if __name__ == '__main__':
    main()
