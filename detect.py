from pitch import funcPitch
from aubio import pitch
# from RMSE import funcRMSE
from PercentSilence import funcPercentSilence
from FrequencyMagnitude import funcFrequencyMagnitude

### % phần trăm khoảng lặng 0,1
### pitch 0,3
### tần số có mật độ lớn nhất 0,3
from attribute import toolHandleAudio
from result import pathAndResult

configPercentSilence = 0.2
# configRMSE = 0.3
configPitch = 0.4
configFrequencyMagnitude = 0.4

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
path = r'C:\Users\84338\OneDrive\Desktop\HTTM\CSDLDPT\test\cat_11.wav' 
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
            compareFile(att1, att)
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






















# att2 = []
# att2.append(toolInstrumentVoice(41.0105, 52.480352808569755, 18.498866213151928, 6044, 752.2972848700547))
# att2.append(toolInstrumentVoice(80.53759, 6.295327728661332, 48.49433106575963, 25529, 144.3187829958743))
# att2.append(toolInstrumentVoice(78.17408, 3.6278046603824587, 47.73242630385488, 45436, 66.06745432748225))
# att2.append(toolInstrumentVoice(79.63045, 3.843097218001882, 48.29478458049886, 70831, 37.561908261746865))
# att2.append(toolInstrumentVoice(78.884094, 7.780515449953133, 49.88208616780045, 108914, 66.06745432748225))
# att2.append(toolInstrumentVoice(80.22667, 5.244177334922521, 49.55555555555555, 128821, 144.3187829958743))
# att2.append(toolInstrumentVoice(80.14571, 7.7701177481295804, 45.35514878292073, 148306, 752.2972848700547))

# print(compareFile(att1, att2))