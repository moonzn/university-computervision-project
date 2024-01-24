from global_variables import *

# Loading the model
model = YOLO(MODEL)

# Image reading and face detection
path = 'CAMINHO DA IMAGEM'
img = cv.imread(path)
results = model.predict(img, verbose=False)
boxes = results[0].boxes
coords = sorted(boxes.xyxy, key=lambda x: x[0])

for index, coord in enumerate(coords):
    confidence = boxes[index].conf.item()
    if confidence < CONFIDENCE_THRESHOLD:
        continue

    # Extracting the image of each person's face
    coord = list(map(round, coord.tolist()))
    face_img = img[coord[1]:coord[3], coord[0]:coord[2]]

    # TODO
    # Carregar classificador de idade e etnia
    # Passar a imagem da cara (face_img)
    # Classificar a pessoa
    # Apresentar na imagem original(?) os resultados obtidos

    # cv.imshow('Imagem Original', img)
    # cv.imshow('Região de Interesse', face_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
