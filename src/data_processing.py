import os
from pathlib import Path
from typing import List
import moviepy.editor as mp
import numpy as np
from pydub import AudioSegment
import moviepy.editor as mp
 


def get_wav_files(directory: str) -> List[str]:
    """Return a list of all WAV files in the given directory."""
    dir_path = Path(directory)
    
    # List all WAV files in the directory
    files = [str(file) for file in dir_path.glob('*.wav') if file.is_file()]
    
    return files

def extract_audio_from_video(video_path, output_dir, sr=32000):
    # Insert Local Video File Path 
    clip = mp.VideoFileClip(video_path)
    
    output_file = os.path.join(output_dir, video_path[:-3] + "wav")
    # Insert Local Audio File Path
    clip.audio.write_audiofile(output_file)

    print("Audio extraction successful!")
    return output_file

def cut_wav_file(input_file, output_dir, segment_length_ms=2000, shift_length_ms=500):
    # Load the audio file
    audio = AudioSegment.from_wav(input_file)
    
    # Get the total length of the audio in milliseconds
    audio_length_ms = len(audio)
    
    # Calculate the number of segments
    num_segments = (audio_length_ms - segment_length_ms) // shift_length_ms + 1
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Cut the audio into segments and save them to files
    segments = []
    times = {}

    for i in range(num_segments):
        start_time = i * shift_length_ms
        end_time = start_time + segment_length_ms
        times[i] = {'start_time': start_time, 'end_time': end_time}

        segment = audio[start_time:end_time]
        
        # Save the segment to a file
        segment_filename = os.path.join(output_dir, f'segment_{i}.wav')
        segment.export(segment_filename, format="wav")
        segments.append(segment_filename)
    
    return segments, times

if __name__ == "__main__":
   # Example usage audio chunks generation:
    data_folder = "../data"
    audio_dir = os.path.join(data_folder, "raw")
    # all_audio_files = get_wav_files(audio_dir)

    #Example use, separate audio from video
    video_path = os.path.join(audio_dir, "harry_potter_example.mp4")
    print(extract_audio_from_video(video_path))

