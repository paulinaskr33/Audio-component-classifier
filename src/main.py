import os
from audio_classifier import AudioClassifier
data_folder = os.path.join(os.getcwd(), '..', 'data')

audio = os.path.join(data_folder, "raw", "home.wav")


classes =["siren", "coughing", "pneumatic hammer"]

clf = AudioClassifier()

values, indices = clf.predict(classes, [audio])


for value, index in zip(values, indices):
    print(f"{classes[index]:>16s}: {100 * value.item():.2f}%")

