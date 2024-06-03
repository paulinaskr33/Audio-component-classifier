import os
import sys
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from audio_classifier import AudioClassifier
from audio_source_separator import SeparateAudio
from audio_chunks import cut_audio_chunk
from dataset import get_wav_files
import pandas as pd
from pydub import AudioSegment

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_model(model_class, *args):
    logging.info(f"Loading model {model_class.__name__}...")
    model = model_class(*args)
    logging.info(f"Model {model_class.__name__} loaded successfully!")
    return model


def process_audio_chunk(audio_chunk_file, sep, clf, classes):
    logging.info(f"Processing audio chunk: {audio_chunk_file}")
    with ThreadPoolExecutor() as inner_executor:
        future_separated_samples = []
        for class_label in classes:
            future_separated_samples.append(inner_executor.submit(
                sep.separate, [audio_chunk_file], class_label))
        for sep_sample_task in as_completed(future_separated_samples):
            sep_sample_task.result()
            
    values, indices = clf.predict(classes, future_separated_samples)
    results = {class_name: 0 for class_name in classes}
    for value, index in zip(values, indices):
        results[classes[index]] = 100 * value.item()
    logging.info(f"Finished processing audio chunk: {audio_chunk_file}")
    return audio_chunk_file, results


def audio_tagging(data_dir, classes):
    logging.info("Starting audio tagging process")

    processed_audio_dir = os.path.join(data_dir, "processed")
    interim_data_dir = os.path.join(data_dir, "interim")
    raw_data_dir = os.path.join(data_dir, "raw")

    with ThreadPoolExecutor() as executor:
        # Load models in parallel
        future_clf = executor.submit(load_model, AudioClassifier)
        future_sep = executor.submit(
            load_model, SeparateAudio, processed_audio_dir)

        clf = future_clf.result()
        sep = future_sep.result()

        logging.info("Models loaded successfully")

        # Load audio files from data/raw
        audio_files = get_wav_files(raw_data_dir)
        logging.info(f"Found {len(audio_files)} audio files")

        futures = []
        for audio_file in audio_files:
            audio_path = os.path.join(raw_data_dir, audio_file)
            audio_segment = AudioSegment.from_wav(audio_path)
            audio_duration_ms = len(audio_segment)
            for chunk_start in range(0, audio_duration_ms, 500):
                audio_chunk = cut_audio_chunk(
                    audio_path, interim_data_dir, chunk_start)
                futures.append(executor.submit(
                    process_audio_chunk, audio_chunk, sep, clf, classes))

        # Initialize an empty DataFrame with columns for filename and each class
        df = pd.DataFrame(columns=['filename'] + classes)

        # Collect results and append to DataFrame
        for future in as_completed(futures):
            audio_chunk_file, results = future.result()
            row = {'filename': audio_chunk_file}
            row.update(results)
            df = df.append(row, ignore_index=True)

        # Save DataFrame to a CSV file
        df.to_csv(os.path.join(
            data_dir, 'audio_classification_results.csv'), index=False)
        logging.info("Results saved to audio_classification_results.csv")


if __name__ == "__main__":
    data_folder = os.path.join(os.getcwd(), '..', 'data')
    with open(os.path.join(data_folder, "sound_classes.txt"), 'r') as file:
        classes = [line.strip() for line in file.readlines()]

    audio_tagging(data_folder, classes)
