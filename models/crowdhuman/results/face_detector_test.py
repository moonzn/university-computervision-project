"""
Deep Learning for Computer Vision - Face detector and classifier by ethnicity and age group

A script to test the Yolov8-Face detector on the CrowdHuman dataset.

Prerequisites:

• Run the preprocessing.py script in "dataset_preparation/crowdhuman" to generate a filtered
version of the CrowdHuman dataset.

• A Yolov8-Face model.

Other models can be used as long as the Path constants are changed in global_variables.py and all other
requirements are met.

This script will detect faces in each image and present the identified faces vs the annotated faces.
The intent is to decide if we need to train our own version of Yolov8.

Authors:
• Bernardo Grilo, n.º 93251
• Gonçalo Carrasco, n.º 109379
• Raúl Nascimento, n.º 87405
"""


from global_variables import *


# Reading the annotation file and structuring it in a dictionary
# The keys are the names of the images and the values are the coordinates of each bounding box
def read_annotations_file():
    data = dict()
    with open(CROWDHUMAN_ANNOTATIONS_PATH, 'r') as f:
        for row in f:
            json_obj = json.loads(row)
            id = json_obj['ID']
            box_list = json_obj['gtboxes']
            data[id] = []
            for box_obj in box_list:
                # Transforms the coordinates of the box into the format (left, top, right, bottom)
                box_coord = box_obj['hbox']
                box_coord[2] = box_coord[0] + box_coord[2]
                box_coord[3] = box_coord[1] + box_coord[3]
                data[id].append(box_coord)

    return data


# Reading the annotations file
annotations = read_annotations_file()

# Loading the model
model = YOLO(YOLO_MODEL)

# To calculate the metrics
max_ious = []
false_positives, true_positives = 0, 0
total_images, total_boxes = 0, 0

# To analyse images one by one
cv_images = []
predicted_boxes = []
annotated_boxes = []

for file in os.listdir(CROWDHUMAN_DIR):
    # Image reading and face detection
    path = os.path.join(CROWDHUMAN_DIR, file)
    img = cv.imread(path)
    results = model.predict(img, verbose=False)
    boxes = results[0].boxes

    prediction_boxes = []
    for box in boxes:
        confidence = box.conf.item()
        if confidence < CONFIDENCE_THRESHOLD:
            continue
        coord = box.xyxy[0]  # Get box coordinates in (left, top, right, bottom) format
        prediction_boxes.append(coord.tolist())

    # Ignores the image if no face is detected
    if len(prediction_boxes) == 0:
        continue

    cv_images.append(img)

    prediction_boxes = sorted(prediction_boxes, key=lambda x: x[0])
    prediction_boxes = torch.tensor(prediction_boxes)
    predicted_boxes.append(prediction_boxes)

    # Boxes of people's faces (ground truth)
    img_id, _ = os.path.splitext(file)
    img_boxes = annotations[img_id]
    img_boxes = torch.tensor(img_boxes)
    annotated_boxes.append(img_boxes)

    # Calculate intersection-over-union (IoU) of boxes
    # The pairwise IoU values for every element in 'img_boxes' and 'prediction_boxes'
    iou_values = metrics.box_iou(prediction_boxes, img_boxes)  # metrics.box_iou(img_boxes, prediction_boxes)
    # Maximum IoU value for each pair of boxes
    max_values, _ = torch.max(iou_values, dim=1)
    max_ious += max_values.tolist()
    true_positives += torch.sum(max_values >= IOU_THRESHOLD).item()  # Above or equal to the IoU threshold
    false_positives += torch.sum(max_values < IOU_THRESHOLD).item()
    total_images += 1
    total_boxes += len(img_boxes)

# Display of metrics in relation to the total bounding boxes of the entire dataset
precision = true_positives / (true_positives + false_positives)
recall = true_positives / total_boxes
f1_score = 2 * (precision * recall) / (precision + recall)
average_iou = sum(max_ious) / len(max_ious)
print(f"After {total_images} images:")  # len(annotations)
print(f"Precision: {round(precision, 3)}"
      f" | Recall: {round(recall, 3)}"
      f" | F1-Score: {round(f1_score, 3)}"
      f" | Average IoU: {round(average_iou, 3)}")

# Draws the bounding boxes and shows each image with the drawn boxes one by one
for idx in range(len(cv_images)):
    img = cv_images[idx]
    pred = predicted_boxes[idx]
    annot = annotated_boxes[idx]

    # Predicted boxes are green
    pred_color = (0, 179, 0)
    pred_thickness = 3
    # Annotated boxes are purple
    annot_color = (179, 0, 179)
    annot_thickness = 2

    img = draw_bounding_boxes(img, pred, pred_color, pred_thickness)
    img = draw_bounding_boxes(img, annot, annot_color, annot_thickness)

    cv.imshow('image', img)
    cv.waitKey(0)
