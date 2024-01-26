import os.path

from global_variables import *

ETHNICITY = ["white", "black", "asian", "indian", "others"]
AGE_GROUP = ["0-2", "3-7", "8-12", "13-19", "20-36", "37-65", "66+"]
TYPE = "blncd"  # age, ethn or blncd (balanced)
DATA_MAX = 0


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


def stats():
    lst = list()
    total_age = [0, 0, 0, 0, 0, 0, 0]
    total_ethn = [0, 0, 0, 0, 0]
    for e in ETHNICITY:
        if TYPE == "blncd":
            print()
        for a in AGE_GROUP:
            dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a)
            match TYPE:
                case "blncd":
                    lst.append(len(dir))
                    print(str(len(dir)) + " people of " + e.upper() + " ethnicity in the age group of " + a)
                case "age":
                    total_age[AGE_GROUP.index(a)] += len(dir)
                case "ethn":
                    total_ethn[ETHNICITY.index(e)] += len(dir)
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
            DATA_MAX = total_age[0]
            print()
            print("The max number of photos per group for a age balanced dataset is " + str(DATA_MAX))
        case "ethn":
            for i in range(len(total_ethn)):
                print(str(total_ethn[i]) + " people of " + ETHNICITY[i].upper() + " ethnicity")
            total_ethn.sort()
            DATA_MAX = total_ethn[0]
            print()
            print("The max number of photos per group for a ethnicity balanced dataset is " + str(DATA_MAX))


def pre_process():
    if os.path.exists(RAW_UTK_PATH):
        if os.path.exists(UTK_PREPROCESSED_DIR):
            shutil.rmtree(UTK_PREPROCESSED_DIR)

        if not os.path.exists(UTK_DATASET_DIR):
            os.makedirs(UTK_DATASET_DIR)
            os.mkdir(UTK_ANNOTATIONS_DIR)

        os.mkdir(UTK_PREPROCESSED_DIR)
        for e in ETHNICITY:
            os.mkdir(UTK_PREPROCESSED_DIR + '\\' + e)
            for a in AGE_GROUP:
                os.mkdir(UTK_PREPROCESSED_DIR + '\\' + e + '\\' + a)

        for filename in os.listdir(RAW_UTK_PATH):
            ethn = int(filename.split('_')[2])
            age = int(filename.split('_')[0])
            shutil.copy(RAW_UTK_PATH + '\\' + filename, UTK_PREPROCESSED_DIR + '\\' + ETHNICITY[ethn] + '\\' + AGE_GROUP[age_group_finder(age)])


def dataset_builder():
    stats()

    if os.path.exists(UTK_DATASET_DIR + '\\' + TYPE):
        shutil.rmtree(UTK_DATASET_DIR + '\\' + TYPE)
        if os.path.exists(UTK_ANNOTATIONS_PATH.split('.')[0] + '_' + TYPE + '.' + UTK_ANNOTATIONS_PATH.split('.')[1]):
            os.remove(UTK_ANNOTATIONS_PATH.split('.')[0] + '_' + TYPE + '.' + UTK_ANNOTATIONS_PATH.split('.')[1])

    os.mkdir(UTK_DATASET_DIR + '\\' + TYPE)
    for e in ETHNICITY:
        for a in AGE_GROUP:
            dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a)
            random.shuffle(dir)
            match TYPE:
                case "blncd":
                    if len(dir) < DATA_MAX:
                        for i in range(len(dir)):
                            shutil.copy(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
                    else:
                        for i in range(DATA_MAX):
                            shutil.copy(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
                case "age":
                    if len(dir) < ceil(DATA_MAX / 5):
                        for i in range(len(dir)):
                            shutil.copy(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
                    else:
                        for i in range(ceil(DATA_MAX / 5)):
                            shutil.copy(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
                case "ethn":
                    if len(dir) < ceil(DATA_MAX / 7):
                        for i in range(len(dir)):
                            shutil.copy(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)
                    else:
                        for i in range(ceil(DATA_MAX / 7)):
                            shutil.copy(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR + '\\' + TYPE)

    f = open(UTK_ANNOTATIONS_PATH.split('.')[0] + '_' + TYPE + '.' + UTK_ANNOTATIONS_PATH.split('.')[1], "x")
    for file in os.listdir(UTK_DATASET_DIR + '\\' + TYPE):
        age = str(age_group_finder(int(file.split('_')[0])))
        ethn = file.split('_')[2]
        f.write("{\"ID\": \"" + file + "\", \"AGE\": " + age + ", \"ETHN\": " + ethn + "}\n")


pre_process()
dataset_builder()
