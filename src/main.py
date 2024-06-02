import os
from audio_classifier import AudioClassifier
from audio_source_separator import SeparateAudio
from audio_chunks import cut_wav_file
from dataset import get_wav_files
import sys

if __name__=="__main__":
    # Add the src directory to the system path
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    data_folder = os.path.join(os.getcwd(), '..', 'data')
    clf = AudioClassifier()
    sep = SeparateAudio(os.path.join(data_folder, "processed"))
    audio_files = get_wav_files(os.path.join(data_folder, "raw"))
    
    # # Open the file in read mode
    with open( os.path.join(data_folder, "sound_classes.txt"), 'r') as file:
        # Read all lines into a list
        classes = file.readlines()

    for audio in audio_files:
        # ## Data prep
        mixed_samples = cut_wav_file(audio,os.path.join(data_folder,"interim"))
        
        # ## Source separation
        separated_samples = sep.separate(mixed_samples,classes)

        ## Classification
        values, indices = clf.predict(classes, audio)
        for value, index in zip(values, indices):
            print(f"{classes[index]:>16s}: {100 * value.item():.2f}%")

