import os
import json
import shutil

# User's Desktop path
DESKTOP_PATH = os.path.join(os.environ['USERPROFILE'], 'Desktop')

# The CrowdHuman dataset should be placed in the user's desktop, in a folder named 'CrowdHuman'
RAW_CROWDHUMAN_PATH = os.path.join(DESKTOP_PATH, 'CrowdHuman')
# Annotations for this dataset
RAW_ANNOTATIONS = 'annotations/annotation_train.odgt'

# Throw error if there is no 'CrowdHuman' folder in the user's desktop
if not os.path.exists(RAW_CROWDHUMAN_PATH):
    exit(f'No dataset found in \'{RAW_CROWDHUMAN_PATH}\'. Please place the dataset in the specified path.')

# Filtered versions will be created in these directories
CROWDHUMAN_DIR = '../../datasets/crowdhuman/dataset'
ANNOTATIONS_DIR = '../../datasets/crowdhuman/annotations'
directories = [CROWDHUMAN_DIR, ANNOTATIONS_DIR]
# The filtered annotations will be stored in this file
CROWDHUMAN_ANNOTATIONS_PATH = '../../datasets/crowdhuman/annotations/crowdhuman_annotations'

# Creates the directories or recreates them
current_directory = os.getcwd()
CROWDHUMAN_PATH = os.path.join(current_directory, CROWDHUMAN_DIR)
print(CROWDHUMAN_PATH)
for dyr in directories:
    if not os.path.exists(dyr):
        os.makedirs(dyr)
    else:
        shutil.rmtree(dyr)
        os.makedirs(dyr)

# Maximum number of people per image
MAX_PEOPLE_PER_IMAGE = 5

number_of_images = 0
number_of_detections = 0
annotations_filtered = ''
with open(f'{RAW_ANNOTATIONS}', 'r') as file:
    for row in file:
        json_obj = json.loads(row)

        # Contagem do número de rostos na fotografia
        bounding_boxes = json_obj['gtboxes']
        n_bounding_boxes = 0
        for bbox in bounding_boxes:
            if bbox['tag'] == 'person' and 'occ' in bbox['head_attr']:
                if bbox['head_attr']['occ'] == 0:
                    n_bounding_boxes += 1

        if n_bounding_boxes <= MAX_PEOPLE_PER_IMAGE:

            filtered_boxes = []
            for bbox in bounding_boxes:
                if bbox['tag'] == 'person' and 'occ' in bbox['head_attr']:
                    if bbox['head_attr']['occ'] == 0:
                        filtered_boxes.append(bbox)

            if filtered_boxes:
                json_obj['gtboxes'] = filtered_boxes
                annotations_filtered += f'{json_obj}\n'
                img_fn = f'{json_obj["ID"]}.jpg'
                shutil.copy(f'{RAW_CROWDHUMAN_PATH}\\{img_fn}', f'{CROWDHUMAN_PATH}\\{img_fn}')
                number_of_images += 1
                number_of_detections += n_bounding_boxes

# Gravação do novo ficheiro de anotações já filtrado
with open(f'{CROWDHUMAN_ANNOTATIONS_PATH}', 'w') as file:
    file.write(annotations_filtered)

print(number_of_detections)
