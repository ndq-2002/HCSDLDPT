import numpy as np
from scipy.io import wavfile
from scipy.signal import get_window
from python_speech_features import mfcc
import os
import csv

# Hàm tính năng lượng trung bình của một khung âm thanh
def compute_energy(frame):
    return np.sum(frame ** 2) / len(frame)

# Hàm tính tần số cơ bản của một khung âm thanh bằng cách sử dụng FFT
def compute_fundamental_frequency(frame, sample_rate):
    fft_spectrum = np.fft.rfft(frame)
    freqs = np.fft.rfftfreq(len(frame), 1/sample_rate)
    peak_index = np.argmax(np.abs(fft_spectrum))
    return freqs[peak_index]

# Hàm trích xuất đặc trưng từ một file âm thanh
def extract_features(audio_path):
    # Đọc file âm thanh
    sample_rate, audio = wavfile.read(audio_path)
    
    # Chuyển âm thanh sang dạng đơn kênh (nếu cần thiết)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    
    # Đặt kích thước khung và độ chồng lấn
    frame_size = int(sample_rate / 20)  # mỗi giây có 20 khung
    hop_size = frame_size // 2  # độ chồng lấn 1/2 khung
    
    frames = []
    for i in range(0, len(audio) - frame_size, hop_size):
        # Áp dụng cửa sổ Hann cho mỗi khung
        frame = audio[i:i + frame_size] * get_window('hann', frame_size)
        frames.append(frame)
    
    mfcc_features = []
    fundamental_frequencies = []
    energies = []

    for frame in frames:
        # Tính toán MFCCs cho mỗi khung
        mfcc_feat = mfcc(frame, samplerate=sample_rate, numcep=13, nfilt=26, nfft=1024*2)
        mfcc_features.append(np.mean(mfcc_feat, axis=0)) # Lấy trung bình MFCCs trên frame
        
        # Tính toán tần số cơ bản cho mỗi khung
        fundamental_frequencies.append(compute_fundamental_frequency(frame, sample_rate))
        
        # Tính toán năng lượng trung bình cho mỗi khung
        energies.append(compute_energy(frame))
    
    return {
        'mfcc': np.array(mfcc_features),
        'fundamental_frequencies': np.array(fundamental_frequencies).reshape(-1, 1),
        'energies': np.array(energies).reshape(-1, 1),
    }
    
# Hàm tổng hợp các đặc trưng bằng cách tính toán các giá trị thống kê
def aggregate_features(features):
    stats = {}
    for key in features:
        data = features[key]
        if data.size > 0:  # Check if data is not empty
            stats[f'{key}_mean'] = np.mean(data, axis=0)
            stats[f'{key}_std'] = np.std(data, axis=0)
            stats[f'{key}_min'] = np.min(data, axis=0)
            stats[f'{key}_max'] = np.max(data, axis=0)
        else:
            # Nếu mảng rỗng, bỏ qua để tránh lỗi
            continue
    
    # Đảm bảo tất cả các mảng đều có số chiều giống nhau
    all_dims = [stats[key].shape for key in stats]
    num_features = max([s[0] if len(s) > 0 else 0 for s in all_dims])  # Lấy số chiều tối đa
    
    # Chuyển đổi các mảng có số chiều khác nhau về cùng số chiều
    for key in stats:
        if stats[key].ndim == 1:
            stats[key] = np.expand_dims(stats[key], axis=0)
        if stats[key].shape[0] < num_features:
            padding = np.zeros((num_features - stats[key].shape[0], stats[key].shape[1]))
            stats[key] = np.vstack((stats[key], padding))
    
    return np.concatenate([stats[key].flatten() for key in stats])
# audio = r'C:\Users\84338\OneDrive\Desktop\HTTM\CSDLDPT\test\cow_10.wav' 
# print(aggregate_features(extract_features(audio)))

# Hàm xử lý tất cả các file âm thanh trong một thư mục
# def process_directory(directory):
#     result = []
#     data = []
#     # for root, _, files in os.walk(directory):
#     #     for filename in files:
#     #         if filename.endswith('.wav'):
#     #             path = os.path.join(root, filename)
#     #             features = extract_features(path)
#     #             aggregated_features = aggregate_features(features)
#     #             data.append(aggregated_features)
#     for filename in os.listdir(directory):
#         if filename.endswith('.wav'):
#             path = os.path.join(directory, filename)
#             features = extract_features(path)
#             aggregated_features = aggregate_features(features)
#             data.append(aggregated_features)
            
    
#     # Tạo tiêu đề cho các cột trong file CSV
#     header = []
#     for key in ['mfcc', 'fundamental_frequencies', 'energies']:
#         num_coeffs = 13 if key == 'mfcc' else 1
#         for i in range(num_coeffs):
#             header += [f'{key}_mean_{i}', f'{key}_std_{i}', f'{key}_min_{i}', f'{key}_max_{i}']
#         # header += [f'{key}_mean_{i}' for i in range(num_coeffs)]
#         # header += [f'{key}_std_{i}' for i in range(num_coeffs)]
#         # header += [f'{key}_min_{i}' for i in range(num_coeffs)]
#         # header += [f'{key}_max_{i}' for i in range(num_coeffs)]
    
#     # listsubpath = []
#     # for x in os.walk(directory):
#     #     listsubpath.append(x[0].replace("\\", "/"))
#     # listsubpath.pop(0)

#     # # get files
#     # allpath = []
#     # for subpath in listsubpath:
#     #     f = []
#     #     for (dirpath, dirnames, filenames) in os.walk(subpath):
#     #         f.extend(filenames)
#     #         break
#     #     for namefile in f:
#     #         allpath.append(subpath + "/" + namefile)
    
#     # Lưu các đặc trưng vào file CSV
#     with open('features.csv', 'w', encoding='UTF8') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(header)
#         # for path in allpath:
#         #     try:
#         #         result = [
#         #             path,
#         #             data 
#         #         ]
#         #         writer.writerow(result)   
#         #     except:
#         #         print("======" + path)
#         #         print('Have exception')
#         writer.writerows(data)
# def process_directories(root_directory):
#     for dirpath, dirnames, _ in os.walk(root_directory):
#         for dirname in dirnames:
#             directory = os.path.join(dirpath, dirname)
#             process_directory(directory)
# # # Gọi hàm xử lý thư mục chứa các file âm thanh
# path = 'C:\\Users\\84338\\OneDrive\\Desktop\\HTTM\\CSDLDPT\\data'
# process_directories(path)

def process_directory(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            path = os.path.join(directory, filename)
            features = extract_features(path)
            aggregated_features = aggregate_features(features)
            # Tạo một từ điển mới bao gồm cả 'file_path' và các phần tử trong aggregated_features
            feature_with_path = {'file_path': filename}
            feature_with_path.update(aggregated_features)
            data.append(feature_with_path)
    return data

def create_csv_header():
    header = ['file_path']
    for key in ['mfcc', 'fundamental_frequencies', 'energies']:
        num_coeffs = 13 if key == 'mfcc' else 1
        for i in range(num_coeffs):
            header += [f'{key}_mean_{i}', f'{key}_std_{i}', f'{key}_min_{i}', f'{key}_max_{i}']
    return header

def process_directories(root_directory):
    csv_header_written = False
    header = create_csv_header()
    
    with open('features.csv', 'w', newline='', encoding='UTF8') as csvfile:
        writer = csv.writer(csvfile)
        
        for dirpath, dirnames, _ in os.walk(root_directory):
            for dirname in dirnames:
                directory = os.path.join(dirpath, dirname)
                data = process_directory(directory)
                
                if data and not csv_header_written:
                    writer.writerow(header)
                    csv_header_written = True
                
                for row in data:
                    row_with_path = [row['file_path']]  # Lấy tên file từ dữ liệu đã trả về
                    for key in ['mfcc', 'fundamental_frequencies', 'energies']:
                        num_coeffs = 13 if key == 'mfcc' else 1
                        row_with_path += row[key]['mean']
                        row_with_path += row[key]['std']
                        row_with_path += row[key]['min']
                        row_with_path += row[key]['max']
                    writer.writerow(row_with_path)

# Call the function with the root directory containing all subdirectories with .wav files
path = 'C:\\Users\\84338\\OneDrive\\Desktop\\HTTM\\CSDLDPT\\data'
process_directories(path)
