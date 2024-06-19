import os
from audio_classifier import AudioClassifier
from audio_source_separator import SeparateAudio
from data_processing import cut_wav_file, extract_audio_from_video
from generate_subtitles import generate_subitles
import dill




def audio_tagging(input_video_file, classes, subtitle_segment_len=4000, subtitle_segment_shift=3000):
    print("Starting audio tagging process")

    processed_data_dir = os.path.join("..", "data", "processed")
    interim_data_dir = os.path.join("..", "data", "interim")
    raw_data_dir = os.path.join("..", "data", "raw")

    ## Load models
    # CLAP
    print("Loading CLAP...")
    clf = AudioClassifier()
    print("CLAP Loaded!")

    # Separate Anything You Describe
    print("Loading Separate Anything You Describe...")
    sep = SeparateAudio()
    print("Separate Anything You Describe loaded!")

    print("Models loaded successfully")


    # Classification results will be stored here
    values = []
    indices = []

    # # Load audio from video file 
    input_audio_file  = extract_audio_from_video(input_video_file, raw_data_dir)
    
    audio_chunks, chunk_times = cut_wav_file(input_audio_file, interim_data_dir, 4000, 3000)

    #audio tagging data will be stored here
    # needed for subtitle creation
    tagging_data = []

    # separate files from interim data dir into processed data dir
    print("Audio source separation in progress...")
    for chunk_idx in range(len(audio_chunks)):
        separated_audio_files = sep.separate(
            [audio_chunks[chunk_idx]],
            processed_data_dir,
            os.path.splitext(os.path.basename(input_video_file))[0] +  "_" + str(chunk_idx),
            classes
        )
        print(f"Separated audio files for chunk {chunk_idx}")
        
        print(f"Starting audio classification....")
        # Classification results will be stored here
        clf_results = dict()
        for class_label in classes:
            clf_results[class_label] = 0.0

        # iterates over all separations made from current chunk
        for separated_audio_file in separated_audio_files:
            
            # classify current separeted file
            values, indices = clf.predict(classes, [separated_audio_file])
            for value, idx in zip(values, indices):
                clf_results[classes[idx]] = max(value.item(), clf_results[classes[idx]])
        
        # getting classes with confidence over 0.5
        best_labels = [] 
        for label_idx in range(len(clf_results)):
            if clf_results[classes[label_idx]] > 0.5:
                best_labels.append(classes[label_idx])

    
        tagging_data.append({
                                'idx' : chunk_idx,
                                'start_time': chunk_times[chunk_idx]['start_time'],
                                'end_time': chunk_times[chunk_idx]['end_time'],
                                'text': ", ".join(best_labels)
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
