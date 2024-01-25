from global_variables import *

TYPE = "ethn"  # age or ethn
SEED = 42  # Seed for split
SPLIT = 0.3  # Fraction of images for validation

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

EPOCHS = 30
history = model.fit(train_ds, epochs=EPOCHS, validation_data=val_ds)

# The trained model is saved to a file.
if not os.path.exists("./models"):
    os.mkdir("./models")
model.save("./models/" + TYPE + ".keras")
