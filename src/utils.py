# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 20:57:02 2023

@author: adam
"""


import os
from unidecode import unidecode
from PIL import Image
import os.path
import  cv2
import numpy as np
from PIL import ImageEnhance
import glob

kernel = np.array([[-1, -1, -1],[-1, 8, -1],[-1, -1, 0]], np.float32) 
kernel = 1/3 * kernel

def crop_and_augment(path):
    dirs = os.listdir(path)
    for item in dirs:
        fullpath = os.path.join(path,item)   
       # fullpath2 = os.path.join(path2,item)   #corrected
        if os.path.isfile(fullpath):
            im = Image.open(fullpath)
            f, e = os.path.splitext(fullpath)
            imCrop = im.crop((0, 0, 1920, 950)) #corrected sometimes 1390, sometimes 950, needs to be automatized

            # resize
            imCrop2 = imCrop.resize((640, 640))
            # augment - flipp
            imCrop3 = np.fliplr(imCrop2)
            
            # enhance sharpness
            imCrop4 = ImageEnhance.Sharpness(imCrop2)
            new_image = imCrop4.enhance(2.0)
            
            # enhance contrast
            imCrop5 = ImageEnhance.Contrast(imCrop2)
            new_image2 = imCrop5.enhance(2.0)
            
            imCrop6 = cv2.filter2D(imCrop3, -1, kernel)
            
            imCrop2.save(f + '_cropped_resized.jpg', "JPEG", quality=100)
            imCrop3 = Image.fromarray(imCrop3)         
            imCrop3.save(f + '_cropped_filpped.jpg', "JPEG", quality=100)
            
            new_image.save(f+ '_cropped_sharped.jpg', quality=100)
            new_image2.save(f+ '_cropped_contrasted.jpg', quality=100)
            
            imCrop6 = Image.fromarray(imCrop6)     
            imCrop6.save(f + '_cropped_filter2d.jpg', "JPEG", quality=100)    
         

def preprocess_1(x):
    x = list(x.split(" "))
    
    return x

def preprocess_2(x):
    x = [float(x1) for x1 in x]
    x[1] = 1-x[1]
    x[0] = int(x[0])
    x= ' '.join(str(e) for e in x)

    return x

def get_image(image_dir, image_name, res_dir):
    count=1
    #for vid in listing:
    vid_name = image_name
    vid = image_dir + vid_name + ".AVI"
    print(vid)
    vidcap = cv2.VideoCapture(vid)
    def get_frame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
            cv2.imwrite(res_dir + unidecode(vid_name) + "_" + str(count) +".jpg", image) # Save frame as JPG file
        return hasFrames
    sec = 0
    frameRate = 10 # Change this number to 1 for each 1 second
    success = get_frame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = get_frame(sec)

def delete_files(path_to_rem):
    files = glob.glob(path_to_rem)
    files = [x for x in files if not '_cropped' in x]
    for f in files:
        os.remove(f)
