from global_variables import *


# Function that converts an age range prediction (integer value) into the corresponding age range
def age_group_finder(age_prediction):
    match age_prediction:
        case 0: return "0-2"
        case 1: return "3-7"
        case 2: return "8-12"
        case 3: return "13-19"
        case 4: return "20-36"
        case 5: return "37-65"
        case 6: return "+66"
        case _: return None


# Loading the models
face_detector = YOLO(MODEL)
age_classifier = tf.keras.models.load_model(AGE_MODEL)
# ethnicity_classifier = tf.keras.models.load_model(ETHNICITY_MODEL)

# Image reading and face detection
path = '273271,1c50900088104e31.jpg'  # 'CAMINHO DA IMAGEM'
img = cv.imread(path)
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

    # PRÉ-PROCESSAMENTO DA IMAGEM

    # Classification of the person's age group
    y_pred_age = age_classifier.predict(face_img)
    print(y_pred_age)
    y_pred_age = tf.argmax(y_pred_age, axis=1)
    print(y_pred_age)

    # Classification of the person's ethnicity
    # y_pred_ethnicity = ethnicity_classifier.predict(face_img)
    # y_pred_ethnicity = tf.argmax(y_pred_ethnicity, axis=1)
    # print(y_pred_ethnicity)

    # TODO
    # Reshape na imagem para o modelo conseguir fazer a predição
    # Classificar a pessoa
    # Apresentar na imagem original(?) os resultados obtidos

    # cv.imshow('Imagem Original', img)
    # cv.imshow('Região de Interesse', face_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
