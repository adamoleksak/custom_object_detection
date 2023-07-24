# my_own_object_detection
Object detection (animal/human) on my custom dataset with yolo v7
## that project assumes such worflow
- extract images from videos
- preprocess extracted images and make image augmentation
- annotate ONLY cropped and resized images, augmented images should be annotated in an automated way by prepare_data script
- use train_fototrap_data.py to fine_tune yolov7 model (paths needs to be fixed, originally I used Colab to train model, that file still needs to be improved)
- example result is stored example_result

