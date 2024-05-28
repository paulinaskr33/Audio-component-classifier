
import os
from typing import List


class SeparateAudio:
    def __init__(self, output_dir: str):
        self.output_directory = output_dir
        os.makedirs(self.output_directory, exist_ok=True)

    def separate(self, file_paths: List[str], sounds_to_separate: List[str]) -> List[str]:
        result_files = []

        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            for sound in sounds_to_separate:
                output_file = os.path.join(self.output_dir, f"{os.path.splitext(file_name)[0]}_{sound}.wav")
                self._separate_sound(file_path, sound, output_file)
                result_files.append(output_file)

        return result_files

    def _separate_sound(self, input_file: str, sound: str, output_file: str):
        model = sep_lib.load_model()  # Load model
        audio_data = sep_lib.load_audio(input_file)  # Load audio file
        separated_audio = model.separate(audio_data, target_sound=sound)  # Source components extraction
        sep_lib.save_audio(output_file, separated_audio)  # Output audio file

# Example use:
if __name__ == "__main__":
    separator = SeparateAudio(output_dir="directory")
    input_files = ["file1.wav", "file2.wav"]
    sounds = ["vocal", "guitar"]
    result = separator.separate(input_files, sounds)
    print("Output files:", result)