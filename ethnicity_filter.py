import os
import shutil

directory = "./UTK"

for filename in os.listdir(directory):
    race = int(filename.split('_')[2])
    match race:
        case 0:
            shutil.copy(directory + '/' + filename, "./ethnicity/white")
        case 1:
            shutil.copy(directory + '/' + filename, "./ethnicity/black")
        case 2:
            shutil.copy(directory + '/' + filename, "./ethnicity/asian")
        case 3:
            shutil.copy(directory + '/' + filename, "./ethnicity/indian")
        case 4:
            shutil.copy(directory + '/' + filename, "./ethnicity/others")
