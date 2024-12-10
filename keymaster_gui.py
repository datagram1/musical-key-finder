import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
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

class KeymasterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keymaster Audio Analyzer")
        self.root.geometry("400x200")

        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Choose file button
        self.choose_button = ttk.Button(main_frame, text="Choose File", command=self.choose_file)
        self.choose_button.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # File path label
        self.file_label = ttk.Label(main_frame, text="No file selected", wraplength=350)
        self.file_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Results frame
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=2, column=0, columnspan=2)

        # Key detection result
        ttk.Label(results_frame, text="Key detected:").grid(row=0, column=0, padx=(0, 10))
        self.key_label = ttk.Label(results_frame, text="-")
        self.key_label.grid(row=0, column=1)

        # BPM detection result
        ttk.Label(results_frame, text="BPM detected:").grid(row=1, column=0, padx=(0, 10))
        self.bpm_label = ttk.Label(results_frame, text="-")
        self.bpm_label.grid(row=1, column=1)

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Audio Files", "*.wav *.mp3 *.aif *.aiff *.flac"),
                ("All Files", "*.*")
            ]
        )

        if file_path:
            self.file_label.config(text=os.path.basename(file_path))
            self.analyze_file(file_path)

    def analyze_file(self, file_path):
        # Change cursor to wait cursor
        self.root.config(cursor="wait")
        self.root.update()

        try:
            # Analyze the audio file
            bpm, key = analyze_single_file(file_path)

            # Update the labels with results
            self.key_label.config(text=key if key else "Error")
            self.bpm_label.config(text=f"{bpm:.2f}" if bpm else "Error")

        except Exception as e:
            self.key_label.config(text="Error")
            self.bpm_label.config(text="Error")
            print(f"Error analyzing file: {e}")

        finally:
            # Change cursor back to normal
            self.root.config(cursor="")

def main():
    root = tk.Tk()
    app = KeymasterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()