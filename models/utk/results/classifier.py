import os
import shutil
import tensorflow as tf
from keras import layers

DATASET_PATH = "../../../datasets/utk/dataset"
TYPE = "age" # age or ethn
SEED = 42  # Seed for split
SPLIT = 0.3  # Fraction of images for validation

labels = list()
annots = open("../../../datasets/utk/annotations/annotations.txt", "r")
for a in annots:
    if TYPE == "age":
        age = int(a.split(',')[1].split(' ')[2])
        labels.append(age)
    else:
        ethn = int(a.split(',')[2].split(' ')[2])
        labels.append(ethn)

train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    labels=labels,
    label_mode='int',
    validation_split=SPLIT,
    subset="both",
    seed=SEED,
    shuffle=True)

model = tf.keras.models.Sequential([
    layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=(256, 256, 3)),
    layers.AveragePooling2D(pool_size=(2, 2)),
    layers.Conv2D(filters=64, kernel_size=3, activation='relu'),
    layers.AveragePooling2D(pool_size=(2, 2)),
    layers.Conv2D(filters=128, kernel_size=3, activation='relu'),
    layers.AveragePooling2D(pool_size=(2, 2)),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu'),
    layers.AveragePooling2D(pool_size=(2, 2)),
    layers.GlobalAveragePooling2D(),
    layers.Dense(132, activation='relu'),
    layers.Dense(7, activation='softmax'),
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

EPOCHS = 15
history = model.fit(train_ds, epochs=EPOCHS, validation_data=val_ds)

if not os.path.exists("./models"):
    os.mkdir("./models")
model.save("./models/" + TYPE + ".keras")
