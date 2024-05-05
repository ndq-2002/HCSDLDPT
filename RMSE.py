import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import IPython.display as ipd
import os

# 700 phần tử, cứ 100 phần tử / 1s
# giá trị đầu tiên bằng trung bình của 100 phần tử

def funcRMSE(file_path):
    FRAME_SIZE = 1024
    HOP_LENGTH = 512
    
    data, samplerate = librosa.load(file_path, duration=7)
    print(samplerate)
    print(len(data))
    rms = librosa.feature.rms(data, frame_length=FRAME_SIZE, hop_length=HOP_LENGTH)[0]
    arr = np.array_split(rms, 7)
    
    result = []
    result = [0 for i in range (7)]
    window = 0
    
    #-----Difference Percentage-----
    for i in range (len(arr)):
        sum = 0
        count = 0 
        for j in range (len(arr[i])-1):
            if(arr[i][j] != 0):
                # TBC hiệu của 2 giá trị cạnh nhau / giá trị tiếp theo để
                # tính năng lượng trung bình ở giá trị tiếp theo lệch bao nhiêu %
                # so với giá trị hiện tại
                sum += ((abs(arr[i][j] - arr[i][j+1]))/arr[i][j])*100
            else: sum+=0
            count+=1
        avg = sum/count
        result[window] = avg
        window+=1
    return result