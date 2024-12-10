#!/usr/bin/env python3.11

import sys
from essentia.standard import RhythmExtractor2013, MonoLoader
from keyfinder import detect_key_librosa
import multiprocessing

def detect_tempo_essentia(audio_file):
    """
    Detects the tempo of an audio file using Essentia.
    """
    try:
        loader = MonoLoader(filename=audio_file)
        audio = loader()
        rhythm_extractor = RhythmExtractor2013(method="multifeature")
        bpm, _, _, _, _ = rhythm_extractor(audio)
        return bpm
    except Exception as e:
        print(f"Error detecting tempo for {audio_file}: {e}")
        return None

def analyze_single_file(file_path):
    """
    Analyzes a single audio file for tempo and key detection.
    """
    bpm = detect_tempo_essentia(file_path)
    key = detect_key_librosa(file_path)
    return bpm, key

def process_audio_files(file_list):
    """
    Processes a list of audio files using multiprocessing.
    """
    with multiprocessing.Pool() as pool:
        results = pool.map(analyze_single_file, file_list)
    return results

def main(file_list):
    """
    Main entry point for the program.
    """
    print("Processing audio files...")
    results = process_audio_files(file_list)
    for file, (bpm, key) in zip(file_list, results):
        print(f"File: {file}")
        print(f" - Detected Tempo: {bpm:.2f} BPM")
        print(f" - Detected Key: {key}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3.11 keymaster.py <file1> <file2> ...")
        sys.exit(1)
    main(sys.argv[1:])