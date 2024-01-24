import os

# User's Desktop path
DESKTOP_PATH = os.path.join(os.environ['USERPROFILE'], 'Desktop')
# (...)\university-computervision-project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------------------------------------------------

# CROWDHUMAN DATASET
# The CrowdHuman dataset should be placed in the user's desktop, in a folder named 'CrowdHuman'
RAW_CROWDHUMAN_PATH = os.path.join(DESKTOP_PATH, 'CrowdHuman')
# Annotations for this dataset
RAW_CROWDHUMAN_ANNOTATIONS_PATH = os.path.join(ROOT_DIR, 'dataset_preparation\\crowdhuman\\annotations\\annotation_train.odgt')

# Filtered versions will be created in these directories
CROWDHUMAN_DIR = os.path.join(ROOT_DIR, 'datasets\\crowdhuman\\dataset')
CROWHUMAN_ANNOTATIONS_DIR = os.path.join(ROOT_DIR, 'datasets\\crowdhuman\\annotations')

# The filtered crowdhuman annotations will be stored in this file
CROWDHUMAN_ANNOTATIONS_PATH = os.path.join(ROOT_DIR, 'datasets\\crowdhuman\\annotations\\crowdhuman_annotations.txt')

# ----------------------------------------------------------------------------------------------------------------------

# UTK DATASET
# The UTK dataset should be placed in the user's desktop, in a folder named 'UTK'
RAW_UTK_PATH = os.path.join(DESKTOP_PATH, 'UTK')

# Filtered version will be created in these directories
UTK_DIR = os.path.join(ROOT_DIR, 'datasets\\utk\\dataset')
UTK_ANNOTATIONS_DIR = os.path.join(ROOT_DIR, 'datasets\\utk\\annotations')

# The filtered UTK annotations will be stored in this file
UTK_ANNOTATIONS_PATH = os.path.join(ROOT_DIR, 'datasets\\crowdhuman\\annotations\\utk_annotations.txt')

