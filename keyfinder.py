import numpy as np
import matplotlib.pyplot as plt
import IPython.display as ipd
import librosa
import librosa.display

# Define complete key profiles for all major and minor keys
KEY_PROFILES_MAJOR = {
    'C':  [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
    'C#': [2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29],
    'D':  [2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66],
    'D#': [3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39],
    'E':  [2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19],
    'F':  [5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52],
    'F#': [2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38, 4.09],
    'G':  [4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33, 4.38],
    'G#': [4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48, 2.33],
    'A':  [2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23, 3.48],
    'A#': [3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35, 2.23],
    'B':  [2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88, 6.35]
}

KEY_PROFILES_MINOR = {
    'C':  [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.42, 3.29],
    'C#': [3.29, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.42],
    'D':  [3.42, 3.29, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69],
    'D#': [2.69, 3.42, 3.29, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98],
    'E':  [3.98, 2.69, 3.42, 3.29, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75],
    'F':  [4.75, 3.98, 2.69, 3.42, 3.29, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54],
    'F#': [2.54, 4.75, 3.98, 2.69, 3.42, 3.29, 6.33, 2.68, 3.52, 5.38, 2.60, 3.53],
    'G':  [3.53, 2.54, 4.75, 3.98, 2.69, 3.42, 3.29, 6.33, 2.68, 3.52, 5.38, 2.60],
    'G#': [2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.42, 3.29, 6.33, 2.68, 3.52, 5.38],
    'A':  [5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.42, 3.29, 6.33, 2.68, 3.52],
    'A#': [3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.42, 3.29, 6.33, 2.68],
    'B':  [2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.42, 3.29, 6.33]
}

def detect_key_librosa(audio_file):
    """
    Detect the musical key of an audio file using Librosa.
    Returns only the key name to maintain compatibility with existing keymaster.py
    """
    try:
        # Load the audio file
        y, sr = librosa.load(audio_file)

        # Compute the chroma feature
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

        # Calculate the average energy for each pitch class
        pitch_class_energy = np.mean(chroma, axis=1)

        # Compare with all key profiles
        correlations = {}

        # Check major keys
        for key, profile in KEY_PROFILES_MAJOR.items():
            correlation = np.corrcoef(pitch_class_energy, profile)[0, 1]
            correlations[f"{key}"] = correlation

        # Check minor keys
        for key, profile in KEY_PROFILES_MINOR.items():
            correlation = np.corrcoef(pitch_class_energy, profile)[0, 1]
            correlations[f"{key}m"] = correlation

        # Find the key with the highest correlation
        detected_key = max(correlations.items(), key=lambda x: x[1])[0]

        return detected_key

    except Exception as e:
        print(f"Error detecting key: {e}")
        return None