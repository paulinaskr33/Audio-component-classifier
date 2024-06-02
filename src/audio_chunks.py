from pydub import AudioSegment
import os

def cut_wav_file(input_file, output_dir, segment_length_ms = 2000, shift_length_ms=200):
    # Load the audio file
    audio = AudioSegment.from_wav(input_file)
    
    # Get the duration of the audio file in milliseconds
    audio_duration_ms = len(audio)
    
    # Calculate the number of segments
    num_segments = (audio_duration_ms - segment_length_ms) // shift_length_ms + 1
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Cut the audio into segments
    output_files = []
    for i in range(num_segments):
        start_time = i * shift_length_ms
        end_time = start_time + segment_length_ms
        segment = audio[start_time:end_time]
        input_file_name = os.path.basename(input_file)
        output_file = os.path.join(output_dir, f"{os.path.splitext(input_file_name)[0]}_segment_{i + 1}.wav")
        segment.export(output_file, format="wav")
        output_files.append(output_file)
        
    return output_files


if __name__ == "__main__":
    # Example usage
    input_file = "../data/raw/home.wav"  # Path to the input WAV file
    output_dir = "."  # Directory to save the output segments
    segment_length_ms = 1000  # Length of each segment in milliseconds (e.g., 5000 ms = 5 seconds)
    shift_length_ms = 900  # Shift length in milliseconds (e.g., 2000 ms = 2 seconds)

    cut_wav_file(input_file, output_dir, segment_length_ms, shift_length_ms)
