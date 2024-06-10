import numpy as np
import librosa
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine

def extract_features(file_path, n_mfcc=13):
    # Tải tín hiệu âm thanh và tần số lấy mẫu
    y, sr = librosa.load(file_path, sr=None)
    
    # Tính toán các đặc trưng cơ bản
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)  # Đặc trưng tần số cơ bản
    energy = librosa.feature.rms(y=y)  # Năng lượng trung bình
    
    # Tính toán MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    
    return pitches, energy, mfccs

def euclidean_distance(vector1, vector2):
    return euclidean(vector1.ravel(), vector2.ravel())  # Làm phẳng ma trận trước khi tính toán

def cosine_similarity(vector1, vector2):
    return 1 - cosine(vector1.ravel(), vector2.ravel())  # Làm phẳng ma trận trước khi tính toán

# Tính toán khoảng cách Euclidean và độ tương tự Cosine giữa các đặc trưng
def compare_features(features1, features2):
    # Tính khoảng cách Euclidean và độ tương tự Cosine cho tần số cơ bản
    pitches_distance = euclidean_distance(features1[0], features2[0])
    pitches_similarity = cosine_similarity(features1[0], features2[0])
    
    # Tính khoảng cách Euclidean và độ tương tự Cosine cho năng lượng trung bình
    energy_distance = euclidean_distance(features1[1], features2[1])
    energy_similarity = cosine_similarity(features1[1], features2[1])
    
    # Tính khoảng cách Euclidean và độ tương tự Cosine cho MFCCs
    mfccs_distance = euclidean_distance(features1[2], features2[2])
    mfccs_similarity = cosine_similarity(features1[2], features2[2])
    
    return pitches_distance, pitches_similarity, energy_distance, energy_similarity, mfccs_distance, mfccs_similarity

# Đường dẫn đến hai tệp âm thanh cần so sánh
file_path1 = r'C:\Users\84338\OneDrive\Desktop\HTTM\CSDLDPT\test\cow_10_out_out.wav'  # 7s audio
file_path2 = r'C:\Users\84338\OneDrive\Desktop\HTTM\CSDLDPT\test\cow_10.wav' 

# Tính toán các đặc trưng từ hai tệp âm thanh
features1 = extract_features(file_path1)
features2 = extract_features(file_path2)

# So sánh các đặc trưng
pitches_distance, pitches_similarity, energy_distance, energy_similarity, mfccs_distance, mfccs_similarity = compare_features(features1, features2)

print("Tần số cơ bản - Khoảng cách Euclidean:", pitches_distance)
print("Tần số cơ bản - Độ tương tự Cosine:", pitches_similarity)
print("Năng lượng trung bình - Khoảng cách Euclidean:", energy_distance)
print("Năng lượng trung bình - Độ tương tự Cosine:", energy_similarity)
print("MFCCs - Khoảng cách Euclidean:", mfccs_distance)
print("MFCCs - Độ tương tự Cosine:", mfccs_similarity)
