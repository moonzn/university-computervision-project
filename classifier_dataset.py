import os
import shutil

utk = "./UTK"
ethnicity = ["white", "black", "asian", "indian", "others"]
age_group = ["0-2", "3-7", "8-12", "13-19", "20-36", "37-65", "66+"]


def directoryInitializer():
    os.mkdir("./classifier")
    for e in ethnicity:
        os.mkdir("./classifier/" + e)
        for a in age_group:
            os.mkdir("./classifier/" + e + "/" + a)


def ageGroupFinder(age):
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


def printStats():
    for e in ethnicity:
        print("\n")
        for a in age_group:
            dir = os.listdir("./classifier/" + e + "/" + a)
            print(str(len(dir)) + " people of " + e.upper() + " ethnicity in the age group of " + a)


if os.path.exists(utk):
    if not os.path.exists("./classifier"):
        directoryInitializer()

    for filename in os.listdir(utk):
        race = int(filename.split('_')[2])
        age = int(filename.split('_')[0])
        shutil.copy(utk + '/' + filename, "./classifier/" + ethnicity[race] + "/" + age_group[ageGroupFinder(age)])

    printStats()
    shutil.rmtree(utk)
