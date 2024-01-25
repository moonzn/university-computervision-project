from global_variables import *

ethnicity = ["white", "black", "asian", "indian", "others"]
age_group = ["0-2", "3-7", "8-12", "13-19", "20-36", "37-65", "66+"]
data_max = 0


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
    for e in ethnicity:
        print()
        for a in age_group:
            dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a)
            lst.append(len(dir))
            print(str(len(dir)) + " people of " + e.upper() + " ethnicity in the age group of " + a)

    lst.sort()
    global data_max
    data_max = lst[8]
    print()
    print("The max number of photos per group for a balanced dataset is " + str(data_max))


def pre_process():
    if os.path.exists(RAW_UTK_PATH):
        if os.path.exists(UTK_PREPROCESSED_DIR):
            shutil.rmtree(UTK_PREPROCESSED_DIR)

        os.mkdir(UTK_PREPROCESSED_DIR)
        for e in ethnicity:
            os.mkdir(UTK_PREPROCESSED_DIR + '\\' + e)
            for a in age_group:
                os.mkdir(UTK_PREPROCESSED_DIR + '\\' + e + '\\' + a)

        for filename in os.listdir(RAW_UTK_PATH):
            ethn = int(filename.split('_')[2])
            age = int(filename.split('_')[0])
            shutil.copy(RAW_UTK_PATH + '\\' + filename, UTK_PREPROCESSED_DIR + '\\' + ethnicity[ethn] + '\\' + age_group[age_group_finder(age)])

        stats()


def dataset_builder():
    if os.path.exists(UTK_DIR):
        shutil.rmtree(UTK_DIR)

    os.makedirs(UTK_DATASET_DIR)
    os.mkdir(UTK_ANNOTATIONS_DIR)
    for e in ethnicity:
        for a in age_group:
            dir = os.listdir(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a)
            random.shuffle(dir)
            if len(dir) < data_max:
                for i in range(len(dir)):
                    shutil.copy(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR)
            else:
                for i in range(data_max):
                    shutil.copy(UTK_PREPROCESSED_DIR + '\\' + e + "\\" + a + "\\" + dir[i], UTK_DATASET_DIR)

    f = open(UTK_ANNOTATIONS_PATH, "x")
    for file in os.listdir(UTK_DATASET_DIR):
        age = str(age_group_finder(int(file.split('_')[0])))
        ethn = file.split('_')[2]
        f.write("{\"ID\": \"" + file + "\", \"AGE\": " + age + ", \"ETHN\": " + ethn + "}\n")


pre_process()
dataset_builder()
