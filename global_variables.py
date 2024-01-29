"""
Deep Learning for Computer Vision - Face detector and classifier by ethnicity and age group

This file contains global variables and functions used in the various scripts developed as part of this project.

Authors:
• Bernardo Grilo, n.º 93251
• Gonçalo Carrasco, n.º 109379
• Raúl Nascimento, n.º 87405
"""

import os
import shutil
import json
import random
import cv2 as cv
import numpy as np
from ultralytics import YOLO
from ultralytics.utils import metrics
import torch
import tensorflow as tf
from keras import layers
import logging
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix
from math import ceil
import pyautogui

# User's Desktop path
DESKTOP_PATH = os.path.join(os.environ['USERPROFILE'], 'Desktop')
# (...)\university-computervision-project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Path with the images that "detector_and_classifier.py" detects the faces and classifies them
IMGS_DIR = os.path.join(ROOT_DIR, 'unclassified_imgs')

# ----------------------------------------------------------------------------------------------------------------------


# CROWDHUMAN DATASET
# The CrowdHuman dataset should be placed in the user's desktop, in a folder named 'CrowdHuman'
RAW_CROWDHUMAN_PATH = os.path.join(DESKTOP_PATH, 'CrowdHuman')
# Annotations for this dataset
RAW_CROWDHUMAN_ANNOTATIONS_PATH = os.path.join(ROOT_DIR,
                                               'dataset_preparation\\crowdhuman\\annotations\\annotation_train.odgt')

# Filtered versions will be created in these directories
CROWDHUMAN_DIR = os.path.join(ROOT_DIR, 'datasets\\crowdhuman\\dataset')
CROWHUMAN_ANNOTATIONS_DIR = os.path.join(ROOT_DIR, 'datasets\\crowdhuman\\annotations')

# The filtered CrowdHuman annotations will be stored in this file
CROWDHUMAN_ANNOTATIONS_PATH = os.path.join(ROOT_DIR, 'datasets\\crowdhuman\\annotations\\crowdhuman_annotations.txt')

# The Yolo face detection model
YOLO_MODEL = os.path.join(ROOT_DIR, 'models\\crowdhuman\\results\\yolov8n-face.pt')
# Threshold for trust in bounding boxes
CONFIDENCE_THRESHOLD = 0.6
# Threshold for the IoU metric
IOU_THRESHOLD = 0.5


# ----------------------------------------------------------------------------------------------------------------------


# UTK DATASET
# The UTK dataset should be placed in the user's desktop, in a folder named 'UTK'
RAW_UTK_PATH = os.path.join(DESKTOP_PATH, 'UTK')

# Filtered version will be created in these directories
UTK_DIR = os.path.join(ROOT_DIR, 'datasets\\utk')
UTK_DATASET_DIR = os.path.join(ROOT_DIR, 'datasets\\utk\\dataset')
UTK_PREPROCESSED_DIR = os.path.join(ROOT_DIR, 'dataset_preparation\\utk\\preprocessed')
UTK_ANNOTATIONS_DIR = os.path.join(ROOT_DIR, 'datasets\\utk\\annotations')

# The filtered UTK annotations will be stored in this file
UTK_ANNOTATIONS_PATH = os.path.join(ROOT_DIR, 'datasets\\utk\\annotations\\utk_annotations.txt')

# Age and ethnicity classification models
AGE_MODEL = os.path.join(ROOT_DIR, 'models\\utk\\results\\models\\ULTIMATE_age.keras')
ETHNICITY_MODEL = os.path.join(ROOT_DIR, 'models\\utk\\results\\models\\AGE_ethn.keras')

ETHNICITY = ["white", "black", "asian", "indian", "others"]
AGE_GROUP = ["0-2", "3-7", "8-12", "13-19", "20-36", "37-65", "66+"]
# ----------------------------------------------------------------------------------------------------------------------


# Function that draws bounding boxes on an image corresponding to the list of coordinates provided
# and which are in the format (x1, y1, x2, y2).
def draw_bounding_boxes(img, boxes, color, thickness):
    for coord in boxes:
        # Represents the top left corner of rectangle
        start_point = (int(coord[0]), int(coord[1]))
        # Represents the bottom right corner of rectangle
        end_point = (int(coord[2]), int(coord[3]))
        img = cv.rectangle(img, start_point, end_point, color, thickness)

    return img
