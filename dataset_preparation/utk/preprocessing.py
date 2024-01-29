"""
Deep Learning for Computer Vision - Face detector and classifier by ethnicity and age group

Preprocessing for the UTK dataset.

Prerequisites:

• A "UTK" folder in the user's desktop containing the UTK dataset, we used a cropped variant.
Note that some images are inconsistently named and will cause errors, these should be deleted.

This script will read the images and their annotations (in this case the file names are the annotations)
and create a filtered dataset inside the project.
The intent is to balance the UTK dataset in different ways to try and get the best results from the classifier.

Authors:
• Bernardo Grilo, n.º 93251
• Gonçalo Carrasco, n.º 109379
• Raúl Nascimento, n.º 87405
"""

from global_variables import *

# The type of balancing, which type gets priority in balancing
TYPE = "blncd"  # age, ethn or blncd (balanced)
DATA_MAX = 0


# How our age groups are defined
def age_group_finder(age):
    if 0 <= age < 3:
        return 0
    elif 3 <= age < 8:
        return 1
    elif 8 <= age < 13:
        return 2
    elif 13 <= age < 20:
        return 3
    elif 20 <= age < 37:
        return 4
    elif 37 <= age < 66:
        return 5
    elif age >= 66:
        return 6


# Function to show the statistics of how the dataset is balanced, after balancing is done
def stats():
    lst = list()
    total_age = [0, 0, 0, 0, 0, 0, 0]
    total_ethn = [0, 0, 0, 0, 0]
    is_age = False
    for e in ETHNICITY:
        match TYPE:
            case "blncd":
                print()
            case "age":
                if ETHNICITY.index(e) > 0:
                    is_age = True
            case "ethn":
                dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e)
                total_ethn[ETHNICITY.index(e)] += len(dir)
        for a in AGE_GROUP:
            if TYPE == "blncd":
                dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e + "\\" + a)
                lst.append(len(dir))
                print(str(len(dir)) + " people of " + e.upper() + " ethnicity in the age group of " + a)
            elif TYPE == "age" and not is_age:
                dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + TYPE + "\\" + a)
                total_age[AGE_GROUP.index(a)] += len(dir)
    global DATA_MAX
    match TYPE:
        case "blncd":
            lst.sort()
            DATA_MAX = lst[ceil((len(lst) / 2) - 1)]
            print()
            print("The max number of photos per group for a true balanced dataset is " + str(DATA_MAX))
        case "age":
            for i in range(len(total_age)):
                print(str(total_age[i]) + " people in the age group of " + AGE_GROUP[i])
            total_age.sort()
            DATA_MAX = total_age[1]
            print()
            print("The max number of photos per group for a age balanced dataset is " + str(DATA_MAX))
        case "ethn":
            for i in range(len(total_ethn)):
                print(str(total_ethn[i]) + " people of " + ETHNICITY[i].upper() + " ethnicity")
            total_ethn.sort()
            DATA_MAX = total_ethn[0]
            print()
            print("The max number of photos per group for a ethnicity balanced dataset is " + str(DATA_MAX))


# Function to split the dataset by age group and ethnicity
def preprocess():
    if os.path.exists(RAW_UTK_PATH):
        if not os.path.exists(UTK_DATASET_DIR):
            os.makedirs(UTK_DATASET_DIR)
            os.mkdir(UTK_ANNOTATIONS_DIR)

        if os.path.exists(UTK_PREPROCESSED_DIR + '\\' + TYPE):
            shutil.rmtree(UTK_PREPROCESSED_DIR + '\\' + TYPE)

        os.makedirs(UTK_PREPROCESSED_DIR + '\\' + TYPE)
        is_age = False
        for e in ETHNICITY:
            if TYPE == "ethn":
                os.mkdir(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e)
            elif TYPE == "age" and ETHNICITY.index(e) > 0:
                is_age = True
            for a in AGE_GROUP:
                if TYPE == "blncd":
                    os.makedirs(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e + '\\' + a)
                elif TYPE == "age" and not is_age:
                    os.mkdir(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + a)

        for filename in os.listdir(RAW_UTK_PATH):
            ethn = int(filename.split('_')[2])
            age = int(filename.split('_')[0])
            match TYPE:
                case "blncd":
                    shutil.copy(RAW_UTK_PATH + '\\' + filename, UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + ETHNICITY[ethn] + '\\' + AGE_GROUP[age_group_finder(age)])
                case "age":
                    shutil.copy(RAW_UTK_PATH + '\\' + filename, UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + AGE_GROUP[age_group_finder(age)])
                case "ethn":
                    shutil.copy(RAW_UTK_PATH + '\\' + filename, UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + ETHNICITY[ethn])


# Function to build the dataset based on the split done by the preprocess function
def dataset_builder():
    stats()

    if os.path.exists(UTK_DATASET_DIR + '\\' + TYPE):
        shutil.rmtree(UTK_DATASET_DIR + '\\' + TYPE)
        if os.path.exists(UTK_ANNOTATIONS_PATH.split('.')[0] + '_' + TYPE + '.' + UTK_ANNOTATIONS_PATH.split('.')[1]):
            os.remove(UTK_ANNOTATIONS_PATH.split('.')[0] + '_' + TYPE + '.' + UTK_ANNOTATIONS_PATH.split('.')[1])

    os.mkdir(UTK_DATASET_DIR + '\\' + TYPE)
    is_age = False
    for e in ETHNICITY:
        if TYPE == "ethn":
            dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e)
            random.shuffle(dir)
            if len(dir) < DATA_MAX:
                for i in range(len(dir)):
                    shutil.copy(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
            else:
                for i in range(DATA_MAX):
                    shutil.copy(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
        elif TYPE == "age" and ETHNICITY.index(e) > 0:
            is_age = True
        for a in AGE_GROUP:
            if TYPE == "blncd":
                dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e + "\\" + a)
                random.shuffle(dir)
                if len(dir) < DATA_MAX:
                    for i in range(len(dir)):
                        shutil.copy(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
                else:
                    for i in range(DATA_MAX):
                        shutil.copy(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
            elif TYPE == "age" and not is_age:
                dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + TYPE + "\\" + a)
                random.shuffle(dir)
                if len(dir) < DATA_MAX:
                    for i in range(len(dir)):
                        shutil.copy(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
                else:
                    for i in range(DATA_MAX):
                        shutil.copy(UTK_PREPROCESSED_DIR + '\\' + TYPE + '\\' + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)

    f = open(UTK_ANNOTATIONS_PATH.split('.')[0] + '_' + TYPE + '.' + UTK_ANNOTATIONS_PATH.split('.')[1], "x")
    for file in os.listdir(UTK_DATASET_DIR + '\\' + TYPE):
        age = str(age_group_finder(int(file.split('_')[0])))
        ethn = file.split('_')[2]
        f.write("{\"ID\": \"" + file + "\", \"AGE\": " + age + ", \"ETHN\": " + ethn + "}\n")


# Runs the functions
preprocess()
dataset_builder()
