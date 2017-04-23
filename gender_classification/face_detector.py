import cv2
from resources.urls import *
from math import sin, cos, radians
import numpy as np
face_cascade = cv2.CascadeClassifier(FRONTAL_FACE_CASCADE)
profile_cascade = cv2.CascadeClassifier(PROFILE_FACE_CASCADE)
body_cascade = cv2.CascadeClassifier(BODY_CASCADE)
eye_cascade = cv2.CascadeClassifier(EYE_CASCADE)

settings = {
    'scaleFactor': 1.03,
    'minNeighbors': 3,
    'minSize': (10, 10),
    'flags': cv2.CASCADE_SCALE_IMAGE,
    'outputRejectLevels': True# cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT| cv2.cv.CV_HAAR_DO_ROUGH_SEARCH
}


def rotate_image(image, angle):
    if angle == 0:
        return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result


def rotate_point(pos, img, angle):
    if angle == 0:
        return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*cos(radians(angle)) + y*sin(radians(angle)) + img.shape[1]*0.4
    newy = -x*sin(radians(angle)) + y*cos(radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]


def detect(img):

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces_result = []
    max_confidence = 0
    max_confident_angle = 0
    max_confident_rects = []

    for angle in [0, 30, -30, 45, 45, 60, -60, 90, -90]:
        rimg = rotate_image(img, angle)
        faces = face_cascade.detectMultiScale3(rimg, **settings)
        rects = faces[0]
        weights = faces[2]

        #print("weights in angle " + str(angle) + ": " + str(weights))
        if len(weights) and weights[0] > max_confidence:
            #print ("max_confidence: " + str(max_confidence) + " update..")
            max_confidence = weights[0]
            max_confident_angle = angle
            max_confident_rects = rects

    if len(max_confident_rects) and max_confidence > 55:
        #print("Angle: " + str(max_confident_angle))
        for face in max_confident_rects:
            #print(max_confidence)
            faces_result.append([rotate_point(face, img, -max_confident_angle)])

        if len(faces_result) != 0:
            #print("Frontal Face")
            return faces_result

    return None


    for angle in [0, -30, 30, -45, 45, 60, -60, 90]:
        rimg = rotate_image(img, angle)
        faces_profile = profile_cascade.detectMultiScale3(rimg, **settings)
        if len(faces_profile):
            print("Angle: " + str(angle))
            for face in faces_profile:
                faces_result.append([rotate_point(face, img, -angle)])
            break

    if len(faces_profile) != 0:
        return faces_result

    for angle in [0, -30, 30, -45, 45, 60, -60, 90]:
        rimg = rotate_image(img, angle)
        bodies = body_cascade.detectMultiScale3(rimg, **settings)
        if len(bodies):
            print("Angle: " + str(angle))
            for body in bodies:
                faces_result.append([rotate_point(body, img, -angle)])
            break

    if len(bodies) != 0:
        print("Body")
        return faces_result

    return None

