import os
import sys
from pipeline import audio_tagging


if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    data_folder = os.path.join(os.getcwd(), '..', 'data')

    #load classes from file
    with open(os.path.join(data_folder, "sound_classes.txt"), 'r') as file:
        classes = [line.strip() for line in file.readlines()]

    audio_tagging(data_folder,classes)

