# Musical Key Finder

A Python project that analyzes audio files to determine their musical key and BPM (beats per minute). This project is forked from [jackmcarthur's musical-key-finder](https://github.com/jackmcarthur/musical-key-finder).

For detailed analysis examples and original implementation details, please refer to the original repository's [musicalkeyfinder.ipynb](https://github.com/jackmcarthur/musical-key-finder/blob/master/musicalkeyfinder.ipynb).

## Features

This fork adds several new capabilities:

- **Graphical User Interface**: Easy-to-use GUI for file selection and analysis
- **BPM Detection**: Tempo detection using the Essentia library
- **JSON Output**: Optional JSON format output for integration with other tools
- **Batch Processing**: Support for analyzing multiple files in succession

## Installation

Requirements:
- Python 3.9+
- Librosa
- Essentia
- NumPy
- tkinter (for GUI version)

```bash
pip install librosa essentia numpy
```

## Usage

### GUI Version
Run the graphical interface with:
```bash
python3 keymaster_gui.py
```

The GUI provides:
- File selection dialog
- Real-time key detection display
- BPM (tempo) detection with 2 decimal precision
- Simple, user-friendly interface

### Command Line Version
For command-line usage:
```bash
python3 keymaster.py <audiofile>
```

Example output:
```
File: song.wav
 - Detected Tempo: 120.45 BPM
 - Detected Key: F# minor
```

### JSON Output
For programmatic integration, use the JSON output version:
```bash
python3 keymaster-json.py <audiofile>
```

Example JSON output:
```json
{
    "key": "F# minor",
    "bpm": "120",
    "bpm_float": "120.45",
    "bpmu": "121",
    "bpmu_float": "120.67",
    "freqs": {
        "C": "0.101",
        "C#": "1.000",
        "D": "0.410"
    }
}
```

## Technical Notes

- Audio analysis works best with samples longer than 10 seconds
- Harmonic-percussive separation is used to improve accuracy
- Supports multiple audio formats (.wav, .mp3, .aif, .aiff, .flac)
- FFmpeg is required for MP3 file analysis

## Acknowledgments

This project builds upon the excellent work by Jack McArthur, extending the original key detection implementation with additional features and interfaces. The original implementation used the Krumhansl-Schmuckler key-finding algorithm for musical key detection.

## License

This project maintains the original license terms while adding new features under the same conditions.