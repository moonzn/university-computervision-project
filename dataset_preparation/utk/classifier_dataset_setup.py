import os
import random
import shutil

utk = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'), 'UTK')
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
            dir = os.listdir("./pre-processed/" + e + "/" + a)
            lst.append(len(dir))
            print(str(len(dir)) + " people of " + e.upper() + " ethnicity in the age group of " + a)

    lst.sort()
    global data_max
    data_max = lst[1]
    print()
    print("The max number of photos per group for a balanced dataset is " + str(data_max))


def pre_process():
    if os.path.exists(utk):
        if os.path.exists("./pre-processed"):
            shutil.rmtree("./pre-processed")

        os.mkdir("./pre-processed")
        for e in ethnicity:
            os.mkdir("./pre-processed/" + e)
            for a in age_group:
                os.mkdir("./pre-processed/" + e + "/" + a)

        for filename in os.listdir(utk):
            ethn = int(filename.split('_')[2])
            age = int(filename.split('_')[0])
            shutil.copy(utk + '/' + filename, "./pre-processed/" + ethnicity[ethn] + "/" + age_group[age_group_finder(age)])

        stats()


def dataset_builder():
    if os.path.exists("../../datasets/utk"):
        shutil.rmtree("../../datasets/utk")

    os.makedirs("../../datasets/utk/dataset")
    os.mkdir("../../datasets/utk/annotations")
    f = open("../../datasets/utk/annotations/annotations.txt", "x")
    for e in ethnicity:
        for a in age_group:
            dir = os.listdir("./pre-processed/" + e + "/" + a)
            random.shuffle(dir)
            if len(dir) < data_max:
                for i in range(len(dir)):
                    id = dir[i].split('_')[3]
                    age = str(age_group_finder(int(dir[i].split('_')[0])))
                    ethn = dir[i].split('_')[2]
                    shutil.copy("./pre-processed/" + e + "/" + a + "/" + dir[i], "../../datasets/utk/dataset")
                    f.write("{\"ID\": " + id + ", \"AGE\": " + age + ", \"ETHN\": " + ethn + "}\n")
            else:
                for i in range(data_max):
                    id = dir[i].split('_')[3]
                    age = str(age_group_finder(int(dir[i].split('_')[0])))
                    ethn = dir[i].split('_')[2]
                    shutil.copy("./pre-processed/" + e + "/" + a + "/" + dir[i], "../../datasets/utk/dataset")
                    f.write("{\"ID\": " + id + ", \"AGE\": " + age + ", \"ETHN\": " + ethn + "}\n")


pre_process()
dataset_builder()
