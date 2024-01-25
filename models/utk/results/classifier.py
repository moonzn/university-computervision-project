from global_variables import *

TYPE = "age"  # age or ethn
if TYPE == "age":
    NUM_CLASSES = 7
else:
    NUM_CLASSES = 5
IMG_HEIGHT = 128
IMG_WIDTH = 128
SEED = 42  # Seed for split
SPLIT = 0.2  # Fraction of images for validation
EPOCHS = 100

# Reading the annotation file and structuring it in a dictionary
data = dict()
for a in open(UTK_ANNOTATIONS_PATH, "r"):
    json_obj = json.loads(a)
    id = json_obj['ID']
    if TYPE == "age":
        data[id] = json_obj['AGE']
    else:
        data[id] = json_obj['ETHN']

# Save the labels in alphanumeric order of the images in the dataset directory
labels = []
for (_, _, files) in os.walk(UTK_DATASET_DIR, topdown=True):
    for fn in files:
        val = data[fn]
        labels.append(val)

train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
    UTK_DATASET_DIR,
    labels=labels,
    label_mode='int',
    validation_split=SPLIT,
    subset="both",
    seed=SEED,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    shuffle=True)

# Define, compile and train model
model = tf.keras.models.Sequential([
    layers.Rescaling(2. / 255, offset=-1, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    layers.RandomFlip("vertical"),
    layers.RandomRotation(0.1),
    layers.Conv2D(filters=64, kernel_size=3, activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(filters=64, kernel_size=3, activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Dropout(0.3),
    layers.Conv2D(filters=128, kernel_size=3, activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Dropout(0.3),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Conv2D(filters=256, kernel_size=3, activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    layers.Dense(NUM_CLASSES, activation='softmax'),
])

model.compile(loss='sparse_categorical_crossentropy', optimizer=tf.keras.optimizers.Nadam(), metrics=['accuracy'])

history = model.fit(train_ds, epochs=EPOCHS, validation_data=val_ds)

plt.figure(num=1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc="upper left")
plt.grid(True, ls='--')
plt.savefig("./models/" + TYPE + "_accuracy.png")

plt.figure(num=2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc="upper right")
plt.grid(True, ls='--')
plt.savefig("./models/" + TYPE + "_loss.png")

plt.show()

# The trained model is saved to a file.
if not os.path.exists("./models"):
    os.mkdir("./models")
model.save("./models/" + TYPE + ".keras")
