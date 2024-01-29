import os.path

from global_variables import *

TYPE = "ethn"  # age, ethn, blncd (balanced) or ultimate (entire UTK)
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


def pre_process():
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


def ultimateAnnotations():
    f = open(UTK_ANNOTATIONS_PATH.split('.')[0] + '_ultimate.' + UTK_ANNOTATIONS_PATH.split('.')[1], "x")
    for file in os.listdir(RAW_UTK_PATH):
        age = str(age_group_finder(int(file.split('_')[0])))
        ethn = file.split('_')[2]
        f.write("{\"ID\": \"" + file + "\", \"AGE\": " + age + ", \"ETHN\": " + ethn + "}\n")


if TYPE == "ultimate":
    ultimateAnnotations()
else:
    pre_process()
    dataset_builder()
