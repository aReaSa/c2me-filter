__author__ = 'raistlin'
import cv2
import glob
from resources.urls import *
from gender_classification import face_detector

image_path = "C:/Users/raistlin/Documents/TensorflowProjects/c2me-filter/user_data/beril/"

for file in glob.glob(image_path + "*.jpg"):
    img = cv2.imread(file)
    img = cv2.resize(img, (200, 200))

    # rows, cols, _ = img.shape
    # M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    # img = cv2.warpAffine(img,M,(cols,rows))

    """
        Image rotations affects face-detector
    """

    faces = face_detector.detect(img)

    if faces is not None:
        for face in faces:
            for (x, y, w, h) in face:
                rec = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                print(str(w) + "x" + str(h))
                roi_gray = img[y:y+h, x:x+w]

    cv2.imshow("img", img)
    cv2.waitKey(0)

