import os
from audio_classifier import AudioClassifier
#from audio_source_separator import SeparateAudio
from audio_chunks import cut_wav_file

if __name__=="__main__":

    data_folder = os.path.join(os.getcwd(), '..', 'data')
    clf = AudioClassifier()
    #sep = SeparateAudio(os.path.join(data_folder, "processed"))
    audio = os.path.join(data_folder, "raw", "home.wav")
    
    # Open the file in read mode
    with open( os.path.join(data_folder, "sound_classes"), 'r') as file:
        # Read all lines into a list
        classes = file.readlines()
    
    # ## Data prep
    # mixed_samples = cut_wav_file(audio,os.path.join(data_folder,"interim"))
    
    # ## Source separation
    # separated_samples = sep.separate(mixed_samples,classes)

    ## Classification
    values, indices = clf.predict(classes, [audio])
    for value, index in zip(values, indices):
        print(f"{classes[index]:>16s}: {100 * value.item():.2f}%")

