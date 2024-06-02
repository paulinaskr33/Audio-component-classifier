import os
import sys
from pathlib import Path
from typing import List
import torch

class SeparateAudio:
    def __init__(self, output_dir):
        # Define output directory relative to the script's directory
        self.output_directory = Path(__file__).resolve().parent / output_dir
        self.output_directory.mkdir(parents=True, exist_ok=True)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Define the checkpoints directory
        self.checkpoints_dir = Path(__file__).resolve().parent / "AudioSep" / "checkpoint"

        # Save the original sys.path
        self.original_sys_path = sys.path.copy()
        
        # Add the AudioSep as githubmodule directory to sys.path
        githubmodule_dir = self.checkpoints_dir.parent
        sys.path.insert(0, str(githubmodule_dir))
        
        # import from AudioSep needs to be made from here because of the sys path changes
        from AudioSep.pipeline import build_audiosep

        models = (
            (
                "https://huggingface.co/spaces/badayvedat/AudioSep/resolve/main/checkpoint/audiosep_base_4M_steps.ckpt",
                self.checkpoints_dir / "audiosep_base_4M_steps.ckpt"
            ),
            (
                "https://huggingface.co/spaces/badayvedat/AudioSep/resolve/main/checkpoint/music_speech_audioset_epoch_15_esc_89.98.pt",
                self.checkpoints_dir / "music_speech_audioset_epoch_15_esc_89.98.pt"
            )
        )

        self.model = build_audiosep(
            config_yaml=str(githubmodule_dir / 'config/audiosep_base.yaml'),
            checkpoint_path=str(models[0][1]),
            device=self.device
        )

        # Restore the original sys.path
        sys.path = self.original_sys_path

    def separate(self, file_paths: List[str], sounds_to_separate: List[str]) -> List[str]:
        # Save the original sys.path
        original_sys_path = sys.path.copy()
        
        # Add the AudioSep as githubmodule directory to sys.path
        githubmodule_dir = self.checkpoints_dir.parent
        sys.path.insert(0, str(githubmodule_dir))
        
        # import from AudioSep needs to be made from here because of the sys path changes
        from AudioSep.pipeline import separate_audio
        
        result_files = []

        for input_file_path in file_paths:
            input_file_name = os.path.basename(input_file_path)
            for sound in sounds_to_separate:
                output_file = self.output_directory / f"{os.path.splitext(input_file_name)[0]}_{sound.replace(' ', '_')}.wav"
                separate_audio(self.model, input_file_path, sound, str(output_file), self.device)
                result_files.append(str(output_file))

        # Restore the original sys.path
        sys.path = original_sys_path
        
        return result_files

# Example use:
if __name__ == "__main__":
    separator = SeparateAudio("../data/processed")
    input_files = ["../data/raw/72a68fda.wav"]
    sounds = ["billard", "ping-pong", "bar"]
    result = separator.separate(input_files, sounds)
    print("Output files:", result)
