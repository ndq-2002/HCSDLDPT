import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean, cosine

def load_audio(file_path):
    # Load the audio file
    y, sr = librosa.load(file_path, sr=None)
    return y, sr

def calculate_mfcc(y, sr, n_mfcc=13):
    # Compute MFCC features
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfccs

def calculate_statistics(mfccs):
    # Calculate statistics of MFCCs
    mfcc_mean = np.mean(mfccs, axis=1)
    mfcc_std = np.std(mfccs, axis=1)
    mfcc_min = np.min(mfccs, axis=1)
    mfcc_max = np.max(mfccs, axis=1)
    mfcc_statistics = np.concatenate((mfcc_mean, mfcc_std, mfcc_min, mfcc_max))
    return mfcc_statistics

def compare_statistics(stats1, stats2):
    # Compare statistics using Euclidean distance and Cosine similarity
    euclidean_distance = euclidean(stats1, stats2)
    cosine_similarity = 1 - cosine(stats1, stats2)
    return euclidean_distance, cosine_similarity

# Load two audio files

file1 = r'C:\Users\84338\OneDrive\Desktop\HTTM\CSDLDPT\test\cow_10_out_out.wav'  # 7s audio
file2 = r'C:\Users\84338\OneDrive\Desktop\HTTM\CSDLDPT\test\cow_10.wav'  # 15s audio

y1, sr1 = load_audio(file1)
y2, sr2 = load_audio(file2)

# Ensure the sample rates are the same
assert sr1 == sr2, "Sample rates are different!"

# Calculate MFCCs for both audio files
mfcc1 = calculate_mfcc(y1, sr1)
mfcc2 = calculate_mfcc(y2, sr2)
print(mfcc1)
print(len(mfcc1))


# Calculate statistics for both MFCCs
stats1 = calculate_statistics(mfcc1)
stats2 = calculate_statistics(mfcc2)

# Compare statistics
euclidean_distance, cosine_similarity = compare_statistics(stats1, stats2)

print(f"Euclidean Distance: {euclidean_distance}")
print(f"Cosine Similarity: {cosine_similarity}")

# Plot MFCCs for visualization
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
librosa.display.specshow(mfcc1, sr=sr1, x_axis='time')
plt.colorbar()
plt.title('MFCCs - Audio 1')

plt.subplot(1, 2, 2)
librosa.display.specshow(mfcc2, sr=sr2, x_axis='time')
plt.colorbar()
plt.title('MFCCs - Audio 2')

plt.tight_layout()
plt.show()
