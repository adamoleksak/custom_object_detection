# my_own_object_detection
Object detection (animal/human) on my custom dataset from camera traps with yolo v7
## that project assumes such worflow
- extract images from videos (_extracted_images_)
- preprocess _extracted_images_ and make image augmentation (_augmented_images_)
- annotate ONLY _extracted_images_, _augmented_images_ should be annotated in an automated way by prepare_data script
- use train_fototrap_data.py to fine_tune yolov7 model (paths needs to be fixed, originally I used Colab to train model, that file still needs to be improved)
- example result is stored example_result

