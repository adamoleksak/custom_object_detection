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
from utils import get_frame, crop_and_augment, delete_files, preprocess_1, preprocess_2


def main():   
    video_path = "../example_image/"
    augmented_images_path = "../example_image/augmented_images_and_labels/"
    cropped_only_path = "../example_image/cropped_only_images_and_labels/"
    
    training_set_path_images = "../example_image/train/images"
    training_set_path_labels = "../example_image/train/labels"
    
    validation_set_path_images = "../example_image/val/images"
    validation_set_path_labels = "../example_image/val/labels"
    
    # get all video files
    all_video = os.listdir(video_path)
    all_video = [i for i in all_video if i.endswith('.mp4')] # sometimes .AVI instead of .mp4
    all_video = [x[:-4] for x in all_video]
    
    # extract images from videos
    [get_frame(image_dir = video_path,
              vid_name = video_name,
              res_dir = augmented_images_path,
              video_format = ".mp4",
              frameRate = 10) for video_name in all_video]
    
    
    # augment images 
    crop_and_augment(augmented_images_path, 13.5)
    
    # drop originally cropped images:
    delete_files(augmented_images_path + '*')
    
    # copy cropped images to different directory to annotate them
    all_cropped = os.listdir(augmented_images_path)
    all_cropped = [image for image in all_cropped if 'cropped_resized.jpg' in image]
    
    for file_name in all_cropped:
        full_file_name = os.path.join(augmented_images_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.move(full_file_name, cropped_only_path)
    
    
    # now it's time to make annotations for images in cropped_only_path
    # select all annotations and annotated images
    all_annotated = os.listdir(cropped_only_path)
    annoattions = [x for x in all_annotated if 'cropped_resized.txt' in x]
    
    # create annotations for non flipped images 
    for file_name in annoattions:
        new_name = file_name[:-11] + "contrasted.txt"
        new_name = os.path.join(augmented_images_path, new_name)
        shutil.copy(os.path.join(cropped_only_path,  file_name), 
                    new_name)
        
    # create annotations for non flipped images 
    for file_name in annoattions:
        new_name = file_name[:-11] + "sharped.txt"
        new_name = os.path.join(augmented_images_path, new_name)
        shutil.copy(os.path.join(cropped_only_path,  file_name), 
                    new_name)
            
    # create annotations for flipped images 
    for file_name in annoattions:
        data_raw = pd.read_csv(cropped_only_path + file_name,
                           header = None)
        
        data_raw = data_raw.apply(lambda x: preprocess_1(x[0]), axis=1)
        data_raw = data_raw.to_frame()
        
        data_raw = data_raw.apply(lambda x: preprocess_2(x[0]), axis=1)
        data_raw = data_raw.to_frame()
        
        data_raw.to_csv(augmented_images_path + file_name[:-11]  + "filpped.txt", header=None, index=None)
        data_raw.to_csv(augmented_images_path + file_name[:-11]  + "filter2d.txt", header=None, index=None)
        
    # copy all files back - from cropped_only_path to augmented_images_path
    
    # getting all the files in the source directory
    cropped_resized_files = os.listdir(cropped_only_path)
    for file_name in cropped_resized_files:
        full_file_name = os.path.join(cropped_only_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, augmented_images_path)
    
    
    
    # todo: create proper val, train, test set split, to avoid having images from the same video in different sets,
    # here simple split as in the example we have only two videos
    all_data = os.listdir(augmented_images_path)
    train = [i for i in all_data if i.startswith(all_video[0])]
    train_images = [i for i in train if i.endswith(".jpg")]
    train_images.append("classes.txt")
    
    train_labels = [i for i in train if i.endswith(".txt")]
    train_labels.append("classes.txt")
    
    val = [i for i in all_data if i.startswith(all_video[1])]
    val_images = [i for i in val if i.endswith(".jpg")]
    val_images.append("classes.txt")
    
    val_labels = [i for i in val if i.endswith(".txt")]
    val_labels.append("classes.txt")
    
    # copy files to train and val directories
    for file_name in train_images:
        full_file_name = os.path.join(augmented_images_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, training_set_path_images)
            
    for file_name in train_labels:
        full_file_name = os.path.join(augmented_images_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, training_set_path_labels)
            
    for file_name in val_images:
        full_file_name = os.path.join(augmented_images_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, validation_set_path_images)
            
    for file_name in val_labels:
        full_file_name = os.path.join(augmented_images_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, validation_set_path_labels)
            
  # todo: create proper val, train, test set split, to avoid having images from the same video in different sets


if __name__ == "__main__":
    main()