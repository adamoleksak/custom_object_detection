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

def crop_and_augment(path, crop_value_from_bottom_in_percents=14):
    dirs = os.listdir(path)
    for item in dirs:
        fullpath = os.path.join(path, item)   
        if os.path.isfile(fullpath):
            im = Image.open(fullpath)
            f, e = os.path.splitext(fullpath)
            new_size = im.size[1] * (100-crop_value_from_bottom_in_percents)/100
            imCrop = im.crop((0, 0, 1920, new_size))

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
    x = ' '.join(str(e) for e in x)
    return x


def get_image(func):
    def wrapper(*args, **kwargs):
        vid = kwargs.get('image_dir') + kwargs.get('vid_name') + kwargs.get('video_format')# ".AVI" #".mp4"
        vidcap = cv2.VideoCapture(vid)
        count = 1
        sec = 0
        frameRate = kwargs.get('frameRate')
        success = func(*args, **kwargs, vidcap = vidcap, count = count, sec = sec)
        video_length_in_seconds = vidcap.get(cv2.CAP_PROP_FRAME_COUNT) / vidcap.get(cv2.CAP_PROP_FPS)
        while (success and sec < (video_length_in_seconds - frameRate)):          
            count = count + 1
            sec =  round(sec + frameRate, 2)
            success = func(*args, **kwargs, vidcap = vidcap, count = count, sec = sec)
    return wrapper


@get_image
def get_frame(image_dir, vid_name, res_dir, vidcap, count, sec, frameRate, video_format, **kwargs):
    vidcap.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        cv2.imwrite(os.path.join(res_dir, unidecode(vid_name) + "_" + str(count) +".jpg"), image) # Save frame as JPG file
    return hasFrames


def delete_files(path_to_rem):
    files = glob.glob(path_to_rem)
    files = [x for x in files if not '_cropped' in x]
    for f in files:
        os.remove(f)
