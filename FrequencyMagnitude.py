import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np

# 700 phần tử. mỗi 1s có 100 p.tử
# giá trị đầu tiên bằng trung bình của 100 phần tử

# Mảng X_mag trả về một mảng bao gồm: 
# Giá trị của phần tử = giá trị magnitude, 
# vị trí của phần tử đó = hz tương ứng => Dùng 2 mảng để lưu lại 2 giá trị đó

def funcFrequencyMagnitude(path):
    #audio, sr = librosa.load(path, duration = 7) #Load file âm thanh vào librosa
    audio, sr = librosa.load(path, sr=None) #Load file âm thanh vào librosa
    X = np.fft.fft(audio) #Mảng X là mảng chứa dãy tần số và mật độ của nó (Mặc định thì độ lớn của mật độ là số ảo ) (Số thực = mật độ / Số ảo = giá trị pha (Ko cần))
    X_mag = np.absolute(X) #Lấy giá trị tuyệt đối thì sẽ có được phần số thực 

    f = np.linspace(0, sr, len(X_mag))
    f_bins = int(len(X_mag))  

    #print(f)
    ################################################3 print(X_mag.size)
    #plt.plot(f[:f_bins], X_mag[:f_bins])
    f[:f_bins], X_mag[:f_bins]

    #print(f)
    #print(X_mag)
    #print(f.size)
    #print(f_bins)
    freq =[] #Freq là mảng ghi tần số có mức độ xuất hiện lớn nhất
    freq = [0 for i in range(7)]

    magnitude =[] #Magnitude là cụ thể mức độ xuất hiện là bao nhiêu
    magnitude = [0 for i in range(7)]

    position = 0
    max = 0
    pos = 0

    for i in range(0, len(X_mag)):        
        if(X_mag[i] > max):
            max = X_mag[i]
            pos = i
        if(i> 0):
            if( (i % int(len(X_mag)/7)) == 0 and i != len(X_mag)-1):            
                freq[position] = pos
                magnitude[position] = max
                #print('Position value at checkpoint: ' + str(position))
                position += 1
                max = 0
            if(i == len(X_mag)-1):            
                freq[position] = pos
                magnitude[position] = max
                #print('Position value at checkpoint: ' + str(position))  

        
    pairs = list(zip(freq, magnitude))
    # print(freq) 
    # print(magnitude)  
    return pairs
