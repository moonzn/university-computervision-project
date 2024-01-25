from global_variables import *

# User's Desktop path
desktop_path = DESKTOP_PATH

# The CrowdHuman dataset should be placed in the user's desktop, in a folder named 'CrowdHuman'
raw_crowdhuman_path = RAW_CROWDHUMAN_PATH
# Annotations for this dataset
raw_annotations = RAW_CROWDHUMAN_ANNOTATIONS_PATH

# Throw error if there is no 'CrowdHuman' folder in the user's desktop
if not os.path.exists(raw_crowdhuman_path):
    exit(f'No dataset found in \'{raw_crowdhuman_path}\'. Please place the dataset in the specified '
         f'path.')

# Filtered versions will be created in these directories
crowdhuman_dir = CROWDHUMAN_DIR
annotations_dir = CROWHUMAN_ANNOTATIONS_DIR
directories = [crowdhuman_dir, annotations_dir]
# The filtered annotations will be stored in this file
crowdhuman_annotations_path = CROWDHUMAN_ANNOTATIONS_PATH

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
with open(f'{RAW_CROWDHUMAN_ANNOTATIONS_PATH}', 'r') as file:
    for row in file:
        json_obj = json.loads(row)

        # Counting the number of faces in the image
        bounding_boxes = json_obj['gtboxes']
        n_bounding_boxes = 0
        for bbox in bounding_boxes:
            if bbox['tag'] == 'person':
                n_bounding_boxes += 1

        if n_bounding_boxes <= max_people_per_image:
            # Cópia da imagem
            img_fn = f"{json_obj['ID']}.jpg"
            shutil.copy(f'{raw_crowdhuman_path}\\{img_fn}', f'{crowdhuman_dir}\\{img_fn}')

            bounding_boxes = [bbox for bbox in bounding_boxes if bbox['tag'] == 'person']
            json_obj['gtboxes'] = bounding_boxes
            annotations_filtered += f'{json_obj}\n'
            number_of_images += 1
            number_of_detections += n_bounding_boxes

# Saving the new filtered annotations file
with open(f'{crowdhuman_annotations_path}', 'w') as file:
    file.write(annotations_filtered.replace("'", "\""))

print(f'Number of images = {number_of_images}')
print(f'Number of faces = {number_of_detections}')