from aubio import source,pitch
import sys
import numpy as np

# 700 phần tử, có 100 phần tử / 1s
# giá trị đầu tiên bằng trung bình của 100 phần tử

# source: dùng để mở tệp âm thanh và cài đặt các thông số cơ bản khác
def funcPitch(path, pitch):
    win_s = 4096 #kích thước cửa sổ cho phân tích tần số
    hop_s = 512  #kích thước bước nhảy giữa các khung âm thanh liên tiếp
    samplerate = 44100 # tần số lấy mẫu của âm thanh 
    tolerance = 0.8 # ngưỡng độ tin cậy
    total_frames = 0 # số lượng mẫu
    
    s = source(path, samplerate, hop_s) 
    samplerate = s.samplerate
    
    pitch_o = pitch("yin", win_s, hop_s, samplerate) # "yin": là thuật toán để tính toán tần số
    pitch_o.set_unit("midi") # đơn vị tính tần số = MIDI
    pitch_o.set_tolerance(tolerance) 
    
    pitches = []
    confidences = []  
    
    
    while True:
        samples, read = s() # lấy mẫu âm thanh và gán = samples, read: chứa số lượng mẫu đọc
        pitch = pitch_o(samples)[0]
        pitches += [pitch] # cộng các pitch với nhau
        confidence = pitch_o.get_confidence()
        confidences += [confidence] # cộng các confidences với nhau
        total_frames += read # cập nhật số lượng mẫu đã đọc được
        if read < hop_s: break

    result = []

    step = int(len(pitches)/7) 

    for i in range(0, 7, 1):
        max = step*(i+1)
        if(i == 6):
            max = len(pitches) - 1
        pitchLocal = []
        for j in range(step*i, max, 1):
            pitchLocal.append(pitches[j])
        result.append(np.array(pitchLocal).mean())  # tính trung bình 

    # print("Average frequency = " + str(np.array(pitches).mean()) + " hz")
    # print(len(result))
    # print(result)
    return result
