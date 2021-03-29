'''
This function includes any kind of image analysis methods

Created by : Dong-gyun KIM
Contact : dong-gyun.kim@awi.de
Creation date : 14.09.2020
'''
from tkinter.filedialog import askdirectory, askopenfilename
from pathlib import Path
from tkinter import Tk
import cv2, os, glob
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

def enhance_contrast (file_path):
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE) # reading in img file
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(8,8)) # enhacne the contrast
    img_enhanced = clahe.apply(img)
    return img_enhanced

def find_contour (file_path):

    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE) # reading in img file
    img_copy = img.copy()
    # remove background 
    unique, counts = np.unique(img_copy, return_counts=True)
    img_dict = dict(zip(unique, counts))
    for intensity, count in img_dict.items():
        if (count > 10000) & (intensity < 10):
            img_copy[img_copy == intensity] = 0

    # Contrast Limited Adaptive Histogram Equalization (CLAHE) for image hacing darka and bright data
    #clahe = cv2.createCLAHE(clipLimit=4, tileGridSize=(8,8)) # enhacne the contrast by Histogram equalization
    #img_enhanced = clahe.apply(img_enhanced)

    blur = cv2.GaussianBlur(img_copy,(5,5),0) # apply blur for contour
    ret, binary = cv2.threshold(blur,1,255,cv2.THRESH_BINARY) # apply threshold to blur image

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # find countour
    
    # detect largest object and return index of the contour
    obj_index = 0
    item_len = 0
    for index, item in enumerate(contours):
        if len(item) > item_len:
            item_len = len(item)
            obj_index = index
        else:
            pass

    contour_img = cv2.drawContours(img_copy, contours, obj_index, (255,0,255), 1) # draw coutour on original image

    cv2.imshow('contours', contour_img)
    cv2.waitKey(500)
    cv2.destroyAllWindows()

    return img, contours, obj_index, binary


def img_values (img, contours, obj_index, binary):
    # return img moments (center and are of objects etc) as dictionary
    moments = cv2.moments(contours[obj_index])
    pixel_area = cv2.contourArea(contours[obj_index]) # calculate pixel area
    
    # area = # calculate area in mm^2

    # calculate gray mean value within contour
    mask_array = np.zeros(img.shape,  np.uint8) # create 0 array having same shape of image
    cv2.drawContours(mask_array, contours, obj_index, 255, -1) # within the contour area convert the value as 255 (white)
    masked_img = np.ma.masked_array(img, mask= (mask_array != 255)) # careful!! 1 is True, 0 is False. in this mask_array, background is False and object is True
    gray_mean = np.mean(masked_img) # unmasked(False=background) will be ignored and masked(Ture=object) will only be considered

    return moments, pixel_area, gray_mean