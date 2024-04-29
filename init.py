from pitch import funcPitch
from aubio import pitch
from RMSE import funcRMSE
import os
from PercentSilence import funcPercentSilence
from FrequencyMagnitude import funcFrequencyMagnitude

listsubpath = []
for x in os.walk('C:\\Users\\84338\\OneDrive\\Desktop\\HTTM\\CSDLDPT\\data'):
    listsubpath.append(x[0].replace("\\", "/"))
listsubpath.pop(0)

# get files
allpath = []
for subpath in listsubpath:
    f = []
    for (dirpath, dirnames, filenames) in os.walk(subpath):
        f.extend(filenames)
        break
    for namefile in f:
        allpath.append(subpath + "/" + namefile)

# write to csv
import csv

with open('data.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    header = ['Path', 'Pitch','FrequencyMagnitude','PercentSilence']
    writer.writerow(header)
    for path in allpath:
        try:
            data = [
                path, 
                funcPitch(path, pitch),
                # funcRMSE(path), 
                funcPercentSilence(path),
                funcFrequencyMagnitude(path)
            ]
            writer.writerow(data)   
        except:
            print("======" + path)
            print('Have exception')

