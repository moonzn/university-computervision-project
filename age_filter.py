import os
import shutil

directory = "./UTK"

for filename in os.listdir(directory):
    age = int(filename.split('_')[0])
    if 0 <= age < 3:
        shutil.copy(directory + '/' + filename, "./age/0-2")
    elif 3 <= age < 8:
        shutil.copy(directory + '/' + filename, "./age/3-7")
    elif 8 <= age < 13:
        shutil.copy(directory + '/' + filename, "./age/8-12")
    elif 13 <= age < 20:
        shutil.copy(directory + '/' + filename, "./age/13-19")
    elif 20 <= age < 37:
        shutil.copy(directory + '/' + filename, "./age/20-36")
    elif 37 <= age < 66:
        shutil.copy(directory + '/' + filename, "./age/37-65")
    elif age >= 66:
        shutil.copy(directory + '/' + filename, "age/66+")
