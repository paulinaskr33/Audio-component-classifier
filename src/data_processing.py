import os
from pathlib import Path
from typing import List
import moviepy.editor as mp
import numpy as np
import librosa
import moviepy.editor as mp
 


def get_wav_files(directory: str) -> List[str]:
    """Return a list of all WAV files in the given directory."""
    dir_path = Path(directory)
    
    # List all WAV files in the directory
    files = [str(file) for file in dir_path.glob('*.wav') if file.is_file()]
    
    return files

def extract_audio_from_video(video_path, sr=32000):
    # Insert Local Video File Path 
    clip = mp.VideoFileClip(video_path)
    
    output_file = video_path[:-3] + "wav"
    # Insert Local Audio File Path
    clip.audio.write_audiofile(output_file )

    print("Audio extraction successful!")
    return output_file

def cut_wav_file(input_file, output_dir, segment_length_ms=2000, shift_length_ms=500, sr=32000):
    # Ensure segment length and shift length are integers
    segment_length_ms = int(segment_length_ms)
    shift_length_ms = int(shift_length_ms)
    
    # Load the audio file
    audio, _ = librosa.load(input_file, sr=sr, mono=True)
    
    # Convert segment length and shift length from milliseconds to samples
    segment_length_samples = int(sr * segment_length_ms / 1000)
    shift_length_samples = int(sr * shift_length_ms / 1000)
    
    # Get the total number of samples in the audio file
    audio_length_samples = len(audio)
    
    # Calculate the number of segments
    num_segments = (audio_length_samples - segment_length_samples) // shift_length_samples + 1
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Cut the audio into segments
    segments = []

    # chunk start and end time (video time)
    times = {}

    for i in range(num_segments):
        start_sample = i * shift_length_samples
        end_sample = start_sample + segment_length_samples
        times[i] = {'start_time': start_sample / sr * 1000, 'end_time': end_sample / sr * 1000}  # Convert samples to milliseconds

        segment = audio[start_sample:end_sample]
        segments.append(segment)

    return segments, times

if __name__ == "__main__":
   # Example usage audio chunks generation:
    data_folder = "../data"
    audio_dir = os.path.join(data_folder, "raw")
    # all_audio_files = get_wav_files(audio_dir)

    #Example use, separate audio from video
    video_path = os.path.join(audio_dir, "harry_potter_example.mp4")
    print(extract_audio_from_video(video_path))

