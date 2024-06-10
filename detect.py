from pitch import funcPitch
from aubio import pitch
# from RMSE import funcRMSE
from PercentSilence import funcPercentSilence
from FrequencyMagnitude import funcFrequencyMagnitude
import numpy as np

### % phần trăm khoảng lặng 0,1
### pitch 0,3
### tần số có mật độ lớn nhất 0,3
from attribute import toolHandleAudio
from result import pathAndResult

configPercentSilence = 0.2
# configRMSE = 0.3
configPitch = 0.4
configFrequencyMagnitude = 0.4



def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def compareFileByCosine(att1, att2):
    max_similarity = 0  # Initialize to the lowest possible similarity (cosine similarity ranges from -1 to 1)
    for i in range(7):
        for j in range(7):
            # Create vectors from attributes
            vec1 = np.array([
                att1[i].PercentSilence,
                att1[i].Pitch,
                att1[i].Magnitude,
                att1[i].Frequency
            ])
            vec2 = np.array([
                att2[j].PercentSilence,
                att2[j].Pitch,
                att2[j].Magnitude,
                att2[j].Frequency
            ])
            # Calculate cosine similarity between the two vectors
            similarity = cosine_similarity(vec1, vec2)
            if max_similarity < similarity:
                max_similarity = similarity
    
    return max_similarity
#--------------------------------------------------------------------------------------------------------------------------
def compareFile(att1, att2): 
    maxRes = 1
    for i in range(7):
        for j in range(7):
            # giongnhau
            same = float(abs(att1[i].PercentSilence - att2[j].PercentSilence) / max(att1[i].PercentSilence, att2[j].PercentSilence) * configPercentSilence)
            # same = same + float(abs(att1[i].RMSE - att2[j].RMSE) / max(att1[i].RMSE, att2[j].RMSE) * configRMSE)
            same = same + float(abs(att1[i].Pitch - att2[j].Pitch) / max(att1[i].Pitch, att2[j].Pitch) * configPitch)
            same = same + float(abs(att1[i].Magnitude - att2[j].Magnitude) / max(att1[i].Magnitude, att2[j].Magnitude) * configFrequencyMagnitude / 2)
            same = same + float(abs(att1[i].Frequency - att2[j].Frequency) / max(att1[i].Frequency, att2[j].Frequency) * configFrequencyMagnitude / 2)
            if(maxRes > same):
                maxRes = same
    
    return maxRes
    
###################################### input ###########################
path = r'C:\Users\84338\OneDrive\Desktop\HTTM\CSDLDPT\test\cow_10.wav' 
# cat_11.wav
# chicken_10.wav
# cow_10.wav
# duck_5.wav
# monkey_8.wav
# rabit_09.wav

att1 = [] 

pitchAtt = funcPitch(path, pitch)
# RMSEAtt = funcRMSE(path)
percentSilenceAtt = funcPercentSilence(path)
frequencyMagnitudeAtt = funcFrequencyMagnitude(path)

magnitudeAtt = []
frequencyAtt = []

for a, b in frequencyMagnitudeAtt:
    magnitudeAtt.append(a)
    frequencyAtt.append(b)
# print(magnitudeAtt)
# print(frequencyAtt)
for i in range(7):
    att1.append(
        toolHandleAudio(
            pitchAtt[i],
            # RMSEAtt[i],
            percentSilenceAtt[i],
            magnitudeAtt[i],
            frequencyAtt[i]
        )
    )
    # print (pitchAtt[i], RMSEAtt[i], percentSilenceAtt[i], magnitudeAtt[i], frequencyAtt[i])

####################################### get data csv #######################
import csv

with open(r'C:\Users\84338\OneDrive\Desktop\HTTM\CSDLDPT\data.csv', 'r', encoding='UTF8') as f:
    reader = csv.reader(f)
    l = [row for row in reader]
    metadata = []
    for row in range(len(l)):
        if row > 1 and row %2 == 0 :
            metadata.append(l[row])


lastResult = []
for i in range(len(metadata)):
    att = []

    Pitch = metadata[i][1].strip("[]").split(', ')
    # RMSE = metadata[i][2].strip("[]").split(', ')
    PercentSilence = metadata[i][2].strip("[]").split(', ')
    frequencyMagnitudeAtt = metadata[i][3].strip("[]").replace("(", "").replace(")", "").split(', ')

    magnitudeAtt = []
    frequencyAtt = []
    for e in range(14):
        if e % 2 == 1:
            frequencyAtt.append(frequencyMagnitudeAtt[e])
        else:
            magnitudeAtt.append(frequencyMagnitudeAtt[e])

    for j in range(7):
        att.append(
            toolHandleAudio(
                float(Pitch[j]),
                # float(RMSE[j]),
                float(PercentSilence[j]),
                float(magnitudeAtt[j]),
                float(frequencyAtt[j])
            )
        )

    lastResult.append(
        pathAndResult(
            "Path: " + metadata[i][0],
            # compareFileByCosine(att1, att)
            compareFile(att1,att)
        )
    )

#### result
    
for i in range(100):
    for j in range(100):
        if(lastResult[i].distance < lastResult[j].distance):
            swap = lastResult[i]
            lastResult[i] = lastResult[j]
            lastResult[j] = swap
print("-----------> Result <----------")
print(lastResult[0].type, lastResult[0].distance)
print(lastResult[1].type, lastResult[1].distance)
print(lastResult[2].type, lastResult[2].distance)
# print(lastResult[3].type, lastResult[3].distance)
# print(lastResult[4].type, lastResult[4].distance)
