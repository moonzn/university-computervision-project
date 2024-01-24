import os
import json
import shutil
import global_variables

# User's Desktop path
desktop_path = global_variables.DESKTOP_PATH

# The CrowdHuman dataset should be placed in the user's desktop, in a folder named 'CrowdHuman'
raw_crowdhuman_path = global_variables.RAW_CROWDHUMAN_PATH
# Annotations for this dataset
raw_annotations = global_variables.RAW_CROWDHUMAN_ANNOTATIONS_PATH

# Throw error if there is no 'CrowdHuman' folder in the user's desktop
if not os.path.exists(raw_crowdhuman_path):
    exit(f'No dataset found in \'{global_variables.RAW_CROWDHUMAN_PATH}\'. Please place the dataset in the specified '
         f'path.')

# Filtered versions will be created in these directories
crowdhuman_dir = global_variables.CROWDHUMAN_DIR
annotations_dir = global_variables.CROWHUMAN_ANNOTATIONS_DIR
directories = [crowdhuman_dir, annotations_dir]
# The filtered annotations will be stored in this file
crowdhuman_annotations_path = global_variables.CROWDHUMAN_ANNOTATIONS_PATH

# Creates the directories or recreates them
for dyr in directories:
    if not os.path.exists(dyr):
        os.makedirs(dyr)
    else:
        shutil.rmtree(dyr)
        os.makedirs(dyr)

# Maximum number of people per image
max_people_per_image = 5

number_of_images = 0
number_of_detections = 0
annotations_filtered = ''
with open(f'{global_variables.RAW_CROWDHUMAN_ANNOTATIONS_PATH}', 'r') as file:
    for row in file:
        json_obj = json.loads(row)

        # Counting the number of faces in the image
        bounding_boxes = json_obj['gtboxes']
        n_bounding_boxes = 0
        for bbox in bounding_boxes:
            if bbox['tag'] == 'person' and 'occ' in bbox['head_attr']:
                if bbox['head_attr']['occ'] == 0:
                    n_bounding_boxes += 1

        if n_bounding_boxes <= max_people_per_image:

            filtered_boxes = []
            for bbox in bounding_boxes:
                if bbox['tag'] == 'person' and 'occ' in bbox['head_attr']:
                    if bbox['head_attr']['occ'] == 0:
                        filtered_boxes.append(bbox)

            if filtered_boxes:
                json_obj['gtboxes'] = filtered_boxes
                annotations_filtered += f'{json_obj}\n'
                img_fn = f'{json_obj["ID"]}.jpg'
                shutil.copy(f'{raw_crowdhuman_path}\\{img_fn}', f'{crowdhuman_dir}\\{img_fn}')
                number_of_images += 1
                number_of_detections += n_bounding_boxes

# Saving the new filtered annotations file
with open(f'{crowdhuman_annotations_path}', 'w') as file:
    file.write(annotations_filtered.replace("'", "\""))

print(f'Number of detections = {number_of_detections}')
