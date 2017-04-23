__author__ = 'raistlin'
import parser
from gender_classification import face_detector
import cv2
import os


# Parses user data from connected2.me, detects faces, writes to file
def obtain_samples():
    MAX_ITER = 100

    has_face_path = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/filtered_shuffle/has_face/"
    image_faces_path = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/filtered_shuffle/has_face/face_images/"

    non_face_path = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/filtered_shuffle/non_face/"
    image_non_faces_path = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/filtered_shuffle/non_face/non_face_images/"

    user_set = set()

    for i in range(0, MAX_ITER):

        user_json = filter_shuffle()
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


def obtain_samples_by_name(name_dict):
    """
    Search users having "key_name", parse all user-data and write under a seperate folder.

    :param name_list: list of preffered names
    :return: None
    """
    USER_DATA_BASE_PATH = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/"
    user_set = set()

    #name_dict = ["beril", "ece", "ayse", "burcu"]

    for _ in range(0, 10):  # 10 Iterations
        print("# iter:  " + str(_))
        for key in name_dict:  # For each name
            user_json = parser.search_shuffle(key)
            for i in range(0, len(user_json["online_users"])):
                nickname = user_json["online_users"][i]["nick"]

                # if user in the set, don't include it again
                if nickname not in user_set:

                    user_set.add(nickname)
                    # low_res_url = user_json["online_users"][i]["images"]["low_res"]
                    hi_res_url = user_json["online_users"][i]["images"]["hi_res"]
                    image = parser.retrieve_profile_picture(hi_res_url)

                    if image is None:
                        continue

                    if not os.path.exists(USER_DATA_BASE_PATH + key):
                        os.makedirs(USER_DATA_BASE_PATH + key)

                    f = open(USER_DATA_BASE_PATH + key + "/" + nickname + '.txt', "w+", encoding="utf-8")
                    f.write(str(user_json["online_users"][i]))
                    f.close()
                    cv2.imwrite(USER_DATA_BASE_PATH + key + "/" + nickname + ".jpg", image)
    return
