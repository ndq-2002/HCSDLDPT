import librosa
import numpy as np

def calculate_average_energy(audio_path):
    # Load the audio file
    y, sr = librosa.load(audio_path)
    
    # Number of samples
    N = len(y)
    
    # Calculate the average energy
    energy = np.sum(y**2) / N
    
    return energy

# Example usage
file_path = r'C:\Users\84338\OneDrive\Desktop\HTTM\CSDLDPT\test\cow_10.wav' 
average_energy = calculate_average_energy(file_path)
print(f"Average energy of the audio file: {average_energy}")
