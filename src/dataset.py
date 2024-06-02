import os
from pathlib import Path
from typing import List

def get_wav_files(directory: str) -> List[str]:
    """Return a list of all WAV files in the given directory."""
    dir_path = Path(directory)
    
    # List all WAV files in the directory
    files = [str(file) for file in dir_path.glob('*.wav') if file.is_file()]
    
    return files

if __name__ == "__main__":
   # Example usage:
    data_folder = "../data"
    audio_dir = os.path.join(data_folder, "raw")
    all_audio_files = get_wav_files(audio_dir)