import librosa

# Thay đổi đường dẫn đến tệp âm thanh của bạn
audio_path = 'C:\\Users\\84338\\OneDrive\\Desktop\\HTTM\\CSDLDPT\\data\\ca\\dolphin.wav'

# Đọc tệp âm thanh và lấy thông tin tần số mẫu
y, sr = librosa.load(audio_path, sr=None)

print("Sample rate:", sr)
