from global_variables import *

DATASET_FOLDER = "CrowdHuman"  # Diretoria do dataset
FILTERED_DATASET_FOLDER = "faces"  # Diretoria onde colocar as imagens que passaram na filtragem
ANNOTATIONS_FN = "annotation_train.odgt"  # Ficheiro de anotações
PERSONS_THRESHOLD = 5  # Nº mínimo de pessoas por fotografia

number_of_images = 0
number_of_detections = 0
annotations_filtered = ""
with open(f'{DATASET_FOLDER}\\{ANNOTATIONS_FN}', 'r') as file:
    for row in file:
        json_obj = json.loads(row)

        # Contagem do número de rostos na fotografia
        bounding_boxes = json_obj['gtboxes']
        n_bounding_boxes = 0
        for bbox in bounding_boxes:
            if bbox['tag'] == 'person':
                n_bounding_boxes += 1

        if n_bounding_boxes <= PERSONS_THRESHOLD:
            # Cópia da imagem
            img_fn = f"{json_obj['ID']}.jpg"
            shutil.copy(f'{DATASET_FOLDER}\\{img_fn}', f'{FILTERED_DATASET_FOLDER}\\{img_fn}')

            bounding_boxes = [bbox for bbox in bounding_boxes if bbox['tag'] == 'person']
            json_obj['gtboxes'] = bounding_boxes
            annotations_filtered += f'{json_obj}\n'
            number_of_images += 1
            number_of_detections += n_bounding_boxes


# Gravação do novo ficheiro de anotações já filtrado
with open(f'{FILTERED_DATASET_FOLDER}\\{ANNOTATIONS_FN}', 'w') as file:
    file.write(annotations_filtered)

# Número de imagens e de rostos do dataset filtrado
print("Number of Images: " + str(number_of_images))
print("Number of Faces: " + str(number_of_detections))
