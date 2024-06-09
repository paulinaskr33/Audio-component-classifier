import os
from audio_classifier import AudioClassifier
from audio_source_separator import SeparateAudio
from data_processing import cut_wav_file, extract_audio_from_video
from generate_subtitles import generate_subitles


def load_model(model_class, *args):
    print(f"Loading model {model_class.__name__}...")
    model = model_class(*args)
    print(f"Model {model_class.__name__} loaded successfully!")
    
    return model


def audio_tagging(input_video_file, classes):
    print("Starting audio tagging process")

    processed_data_dir = os.path.join("..", "data", "processed")
    interim_data_dir = os.path.join("..", "data", "interim")

    # Load models
    clf = load_model(AudioClassifier)
    sep = load_model(SeparateAudio, processed_data_dir)
    print("Models loaded successfully")


    # Classification results will be stored here
    values = []
    indices = []

    # # Load audio from video file 
    input_audio_file  = extract_audio_from_video(input_video_file)
    
    audio_chunks, chunk_times = cut_wav_file(input_audio_file, interim_data_dir)

    #audio tagging data will be stored here
    # needed for subtitle creation
    tagging_data = []

    # separate files from interim data dir into processed data dir
    for chunk_idx in range(len(audio_chunks)):
        separated_audio_files = sep.separate(
            audio_chunks,
            os.path.splitext(os.path.basename(input_video_file))[0] +  "_" + str(chunk_idx),
            classes
        )
        print(f"Separated audio files for chunk {chunk_idx}")
        
        # Classification results will be stored here
        clf_results = dict()
        for class_label in classes:
            clf_results[class_label] = 0.0

        # iterates over all separations made from current chunk
        for separated_audio_file in separated_audio_files:
            
            # classify current separeted file
            values, indices = clf.predict(classes, [separated_audio_file])
            for value, idx in zip(values, indices):
                clf_results[classes[idx]] = min(value.item(), clf_results[classes[idx]])
        # sorting class labels by confidence   
        clf_results = sorted(clf_results.items(), key=lambda x:x[1])
       
        print(clf_results)
        # getting only the class label with best confidence for given chunk
        # and the best confidence must be at least 0.5
        if clf_results[0][1] > 0.5:
            text = clf_results[0][0]
        else:
            text = ""
        tagging_data.append({
                                'idx' : chunk_idx,
                                'start_time': chunk_times[chunk_idx]['start_time'],
                                'end_time': chunk_times[chunk_idx]['end_time'],
                                'text': clf_results[0][0],
                                'confidence': clf_results[0][1]
                            })

        print(f"Recognized audio source for chunk {chunk_idx}:")
        print(f"{tagging_data[chunk_idx]['text']}")

    return generate_subitles(
        tagging_data,  
        os.path.splitext(os.path.basename(input_video_file))[0]
        )
    


if __name__ == "__main__":
    data_folder = os.path.join(os.getcwd(), '..', 'data', "raw")
    input_file = os.path.join(data_folder, "72a68fda.wav")
    with open(os.path.join(data_folder, "..", "sound_classes.txt"), 'r') as file:
        classes = [line.strip() for line in file.readlines()]

    audio_tagging(input_file, classes)
