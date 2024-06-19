import os
import sys
from pathlib import Path
from typing import List
import torch
import subprocess
import dill



class SeparateAudio:
    def __init__(self):
        
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Define the checkpoints directory
        self.checkpoints_dir = Path(__file__).resolve().parent / "AudioSep" / "checkpoint"
        if not os.path.exists(self.checkpoints_dir):
            os.makedirs(self.checkpoints_dir)
       

        # Save the original sys.path
        self.original_sys_path = sys.path.copy()
    

        # =================== change directory to AudioSep =======================
        # Add AudioSep to sys.path
        module_dir = self.checkpoints_dir.parent
        sys.path.insert(0, str(module_dir))

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

        
        # Check if model weights are downloaded
        # if not donwload them
        for model_url, model_path in models:
            if not model_path.exists():
                print(f"\tNo AudioSep model weights found for {model_path}. Downloading now...")
                # Example command: list the contents of the current directory on Windows
                command = f"wget {model_url} -O {model_path}"
                # Run the command
                result = subprocess.run(command, capture_output=True, text=True, shell=True)
                # Print the output
                print(result.stdout)
        
        # import from AudioSep needs to be made from here because of the sys path changes
        from AudioSep.pipeline import build_audiosep

        self.model = build_audiosep(
            config_yaml=str(module_dir / 'config/audiosep_base.yaml'),
            checkpoint_path=str(models[0][1]),
            device=self.device
        )

        # =================== change directory to src =======================
        # Restore the original sys.path
        sys.path = self.original_sys_path

    def separate(self, audio_samples, output_dir, output_file_prefix, sounds_to_separate ) -> List[str]:
        # Define output directory relative to the script's directory
        output_directory = Path(__file__).resolve().parent / output_dir
        output_directory.mkdir(parents=True, exist_ok=True)

        # Save the original sys.path
        original_sys_path = sys.path.copy()
        
        # Add the AudioSep as module directory to sys.path
        module_dir = self.checkpoints_dir.parent
        sys.path.insert(0, str(module_dir))
        
        # import from AudioSep needs to be made from here because of the sys path changes
        from AudioSep.pipeline import separate_audio
        
        result_files = []

        for audio in audio_samples:
            for sound in sounds_to_separate:
                label = sound.replace(" ", "_")
                output_file = output_directory / f"{output_file_prefix}_{label}.wav"
                separate_audio(self.model, audio, sound, str(output_file), self.device, use_chunk=False)
                result_files.append(str(output_file))
        print("\t audio samples processed")
        # Restore the original sys.path
        sys.path = original_sys_path
        
        return result_files

# Example use:
if __name__ == "__main__":
    separator = SeparateAudio()
    
