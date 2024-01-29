"""
Deep Learning for Computer Vision - Face detector and classifier by ethnicity and age group

Training and generation of age/ethnicity classification model using a convolutional neural network.

Prerequisites:

• Run the preprocessing.py file in "dataset_preparation/utk" to generate the UTK dataset filtered and
ready to train the models.
• Change the TYPE and DATASET variables to choose which type of classifier you want to generate (age group or ethnicity)
and with which type of dataset filtering you want to train the models.

This script will read the annotations from the filtered dataset chosen for training and will train a convolutional
neural network with the images from that dataset.
After training, the accuracy and loss function graphs corresponding to the training and validation set are displayed.
The trained model is saved, ready for use.

Authors:
• Bernardo Grilo, n.º 93251
• Gonçalo Carrasco, n.º 109379
• Raúl Nascimento, n.º 87405
"""

from global_variables import *

logging.disable(logging.WARN)
logging.disable(logging.INFO)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# -----------------------------------------------------------------------------------------------------
# Read and prepare dataset

TYPE = "ethn"  # age or ethn
DATASET = "ethn"  # age, ethn or blncd
NUM_CLASSES = 7 if TYPE == "age" else 5
IMG_HEIGHT = 128
IMG_WIDTH = 128
SEED = 42  # Seed for split
SPLIT = 0.2  # Fraction of images for validation
EPOCHS = 100

# Reading the annotation file and structuring it in a dictionary
data = dict()
for a in open(UTK_ANNOTATIONS_PATH.split('.')[0] + '_' + DATASET + '.' + UTK_ANNOTATIONS_PATH.split('.')[1], "r"):
    json_obj = json.loads(a)
    id = json_obj['ID']
    data[id] = json_obj[TYPE.upper()]

# Save the labels in alphanumeric order of the images in the dataset directory
labels = []
for file in os.listdir(UTK_DATASET_DIR + '\\' + DATASET):
    val = data[file]
    labels.append(val)

train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
    UTK_DATASET_DIR + '\\' + DATASET,
    labels=labels,
    label_mode='int',
    validation_split=SPLIT,
    subset="both",
    seed=SEED,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    shuffle=True)

callback = tf.keras.callbacks.EarlyStopping(monitor="val_loss", mode="min", patience=10)

# Define, compile and train model
model = tf.keras.models.Sequential([
    layers.Rescaling(2. / 255, offset=-1, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.125),
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
    layers.Dropout(0.5),
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
history = model.fit(train_ds, epochs=EPOCHS, validation_data=val_ds, callbacks=[callback])

if not os.path.exists("./models"):
    os.mkdir("./models")

plt.figure(num=1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc="upper left")
plt.grid(True, ls='--')
plt.savefig("./models/" + DATASET.upper() + '_' + TYPE + "_accuracy.png")

plt.figure(num=2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc="upper right")
plt.grid(True, ls='--')
plt.savefig("./models/" + DATASET.upper() + '_' + TYPE + "_loss.png")
plt.show()

# The trained model is saved to a file.
model.save("./models/" + DATASET.upper() + '_' + TYPE + ".keras")
