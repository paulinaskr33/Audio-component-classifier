import os
from pipeline import audio_tagging


if __name__ == "__main__":
    data_folder = os.path.join(os.getcwd(), '..','data', "raw")
    input_file = os.path.join(data_folder, "harry_potter_example.mp4")
    with open(os.path.join(data_folder, "..","sound_classes.txt"), 'r') as file:
        classes = [line.strip() for line in file.readlines()]

    audio_tagging(input_file, classes)

