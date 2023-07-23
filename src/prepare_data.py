# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 22:31:55 2022

@author: adam
"""


import os
import shutil
import random
import pandas as pd
from collections import Counter
from utils import get_image, crop_and_augment, delete_files, preprocess_1, preprocess_2

video_path = "example_image/"
extracted_images_path = "example_image/augmented_images_and_labels/"
cropped_only_path = "example_image/cropped_only_images_and_labels/"

# get all video files
all_video = os.listdir(video_path)
all_video = [i for i in all_video if i.endswith('.AVI')] # sometimes mp3 instead of AVI
all_video = [x[:-4] for x in all_video]
all_video.sort()

# extract images from videos
[get_image(video_path,
          x,
          res_dir = extracted_images_path) for x in all_video]

# augment images 
crop_and_augment(extracted_images_path)

# drop originally cropped images:
delete_files(extracted_images_path + '*')

# copy cropped images to different dir to annotate them
all_cropped = os.listdir(extracted_images_path)
all_cropped = [x for x in all_cropped if 'cropped_resized.jpg' in x]

for file_name in all_cropped:
    full_file_name = os.path.join(extracted_images_path, file_name)
    if os.path.isfile(full_file_name):
        shutil.move(full_file_name, cropped_only_path)


# now it's time to make annotations for images in cropped_only_path
# select all annotations and annotated images
all_annotated = os.listdir(cropped_only_path)

# get only jpg annotated names
jpg_files_annotated = [x[:-3] + "jpg" for x in all_annotated]
jpg_files_annotated = list(Counter(jpg_files_annotated))

# manage annotations
all_annotated = os.listdir(cropped_only_path)
# remove possible existing 'classes.txt" file

annoattions = [x for x in all_annotated if 'cropped_resized.txt' in x]
cropped_only_path
# select annotated files and autimatically create annotation files
# manage non flipped coordinates 
for file_name in annoattions:
    new_name = file_name[:-11]+ "contrasted.txt"
    new_name = os.path.join(extracted_images_path, new_name)
    shutil.copy(os.path.join(cropped_only_path,  file_name), 
                new_name)
    
# manage flipped coordinates by changing one of the coordinates 
for file_name in annoattions:
    new_name = file_name[:-11]+ "sharped.txt"
    new_name = os.path.join(extracted_images_path, new_name)
    shutil.copy(os.path.join(cropped_only_path,  file_name), 
                new_name)
        
# manage flipped coordinates by changing one of the coordinates 
for file_name in annoattions:
    data_raw = pd.read_csv(cropped_only_path + file_name,
                       header = None)
    
    x = data_raw.apply(lambda x: preprocess_1(x[0]), axis=1)
    x = x.to_frame()
    
    x2 = x.apply(lambda x: preprocess_2(x[0]), axis=1)
    x3 = x2.to_frame()
    
    x3.to_csv(extracted_images_path + file_name[:-11]  + "filpped.txt", header=None, index=None)
    x3.to_csv(extracted_images_path + file_name[:-11]  + "filter2d.txt", header=None, index=None)


# todo: create proper val, train, test set split, to avoid having images from the same video in different sets
