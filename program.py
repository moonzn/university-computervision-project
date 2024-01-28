from global_variables import *

# Loading the models
face_detector = YOLO(MODEL)
age_classifier = tf.keras.models.load_model(AGE_MODEL)
ethnicity_classifier = tf.keras.models.load_model(ETHNICITY_MODEL)

# Image reading and face detection
imgs = os.listdir(IMGS_DIR)
random.shuffle(imgs)
for file in imgs:
    img = cv.imread(os.path.join(IMGS_DIR, file))
    results = face_detector.predict(img, verbose=False)
    boxes = results[0].boxes
    coords = sorted(boxes.xyxy, key=lambda x: x[0])

    for index, coord in enumerate(coords):
        confidence = boxes[index].conf.item()
        if confidence < CONFIDENCE_THRESHOLD:
            continue

        # Extracting the image of each person's face
        coord = list(map(round, coord.tolist()))
        face_img = img[coord[1]:coord[3], coord[0]:coord[2]]
        face_img = cv.resize(face_img, (128, 128))
        face_img = np.expand_dims(face_img, axis=0)

        # PRÉ-PROCESSAMENTO DA IMAGEM

        # Classification of the person's age group
        y_pred_age = age_classifier.predict(face_img)
        print(y_pred_age)
        pred_age = tf.argmax(y_pred_age, axis=1)
        a = tf.get_static_value(pred_age[0])
        print(str(y_pred_age[0][a]) + " probability of being in the age group of " + AGE_GROUP[a])

        # Classification of the person's ethnicity
        y_pred_ethn = ethnicity_classifier.predict(face_img)
        print(y_pred_ethn)
        pred_ethn = tf.argmax(y_pred_ethn, axis=1)
        e = tf.get_static_value(pred_ethn[0])
        print(str(y_pred_ethn[0][e]) + " probability of being " + ETHNICITY[e].upper())

        label1 = AGE_GROUP[a] + ": " + str(round(y_pred_age[0][a] * 100, 1)) + "%"
        label2 = ETHNICITY[e].upper() + ": " + str(round(y_pred_ethn[0][e] * 100, 1)) + "%"
        (w, h), _ = cv.getTextSize(label2, cv.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        text_bg = cv.rectangle(img, (coord[0], coord[1] - 45), (coord[0] + w + 5, coord[1]), (179, 0, 179), -1)
        img = draw_bounding_boxes(img, [coord], (179, 0, 179), 2)
        img = cv.putText(img, label1, (coord[0], coord[1] - 5), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        img = cv.putText(img, label2, (coord[0], coord[1] - 27), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    screen_w, screen_h = pyautogui.size()
    if img.shape[0] > screen_h or img.shape[1] > screen_w:
        img = cv.resize(img, (0, 0), fx=0.4, fy=0.4)
    cv.imshow('Image', img)
    cv.waitKey(0)
