import os
import streamlit as st
import soundfile as sf
import numpy as np
import librosa
import pandas as pd
import random
import shutil
from pydub import AudioSegment


def modify_audio(file_path, initial_duration, end_duration, pre_roll, operation):
    # Load the audio file
    audio, sr = sf.read(file_path)

    # Calculate the reduction durations
    reduction_initial = initial_duration - pre_roll
    reduction_end = end_duration - pre_roll

    # Perform the specified operation based on the button selection
    if operation == "Trim Beginning":
        # Check if initial silence duration is longer
        if reduction_initial > 0:
            # Calculate the number of samples to remove based on the reduction duration
            reduction_samples_initial = int(reduction_initial * sr)

            # Trim the audio from the beginning to reach the pre-roll length
            modified_audio = audio[reduction_samples_initial:]
        else:
            # No trimming required
            modified_audio = audio

    elif operation == "Trim End":
        # Check if end silence duration is longer
        if reduction_end > 0:
            # Calculate the number of samples to remove based on the reduction duration
            reduction_samples_end = int(reduction_end * sr)

            # Trim the audio from the end to reach the pre-roll length
            modified_audio = audio[:-reduction_samples_end]
        else:
            # No trimming required
            modified_audio = audio

    elif operation == "Pad Beginning":
        # Check if initial silence duration is shorter
        if reduction_initial < 0:
            # Calculate the difference in length required to reach the pre-roll value
            diff_initial = pre_roll - initial_duration

            # Calculate the number of samples to add based on the difference in length
            add_samples_initial = int(diff_initial * sr)

            # Pad the beginning of the audio with zeros by adding the specified number of samples
            if audio.ndim > 1:
                initial_zeros = np.zeros((add_samples_initial, audio.shape[1]), dtype=audio.dtype)
            else:
                initial_zeros = np.zeros(add_samples_initial, dtype=audio.dtype)
            modified_audio = np.concatenate((initial_zeros, audio), axis=0)
        else:
            # No padding required
            modified_audio = audio

    elif operation == "Pad End":
        # Check if end silence duration is shorter
        if reduction_end < 0:
            # Calculate the difference in length required to reach the pre-roll value
            diff_end = pre_roll - end_duration

            # Calculate the number of samples to add based on the difference in length
            add_samples_end = int(diff_end * sr)

            # Pad the end of the audio with zeros by adding the specified number of samples
            if audio.ndim > 1:
                end_zeros = np.zeros((add_samples_end, audio.shape[1]), dtype=audio.dtype)
            else:
                end_zeros = np.zeros(add_samples_end, dtype=audio.dtype)
            modified_audio = np.concatenate((audio, end_zeros), axis=0)
        else:
            # No padding required
            modified_audio = audio

    else:
        # Invalid operation
        print(f"Invalid operation: {operation}")
        return None

    # Create the processed folder path
    processed_folder = "./processed"
    os.makedirs(processed_folder, exist_ok=True)

    # Create a modified file name
    file_name = os.path.basename(file_path)
    modified_file_name = file_name.replace(".wav", f"_{operation.replace(' ', '_').lower()}.wav")
    # Create the modified file path
    modified_file_path = os.path.join(processed_folder, modified_file_name)

    # Save the modified audio as a new WAV file with the same parameters as the input
    sf.write(modified_file_path, modified_audio, sr, subtype='PCM_24')

    return modified_file_path

def trim_beginning(file_path, initial_duration, pre_roll):
    # Load the audio file
    audio, sr = sf.read(file_path)

    # Calculate the number of samples to remove based on the difference between initial duration and pre roll
    reduction_samples_initial = int((initial_duration - pre_roll) * sr)

    # Trim the beginning of the audio by removing the specified number of samples
    modified_audio = audio[reduction_samples_initial:]

    # Create the processed folder path
    processed_folder = "./output/trim_beginning"
    os.makedirs(processed_folder, exist_ok=True)

    # Create a modified file name
    file_name = os.path.basename(file_path)
    modified_file_name = file_name.replace(".wav", ".wav")

    # Create the modified file path
    modified_file_path = os.path.join(processed_folder, modified_file_name)

    # Save the modified audio as a new WAV file with the same parameters as the input
    sf.write(modified_file_path, modified_audio, sr, subtype='PCM_24')

    return modified_file_path

def trim_end(file_path, end_duration, pre_roll):
    # Load the audio file
    audio, sr = sf.read(file_path)

    # Calculate the number of samples to remove based on the difference between end duration and pre roll
    reduction_samples_end = int((end_duration - pre_roll) * sr)

    # Trim the end of the audio by removing the specified number of samples
    modified_audio = audio[:-reduction_samples_end]

    # Create the processed folder path
    processed_folder = "./output/trim_end"
    os.makedirs(processed_folder, exist_ok=True)

    # Create a modified file name
    file_name = os.path.basename(file_path)
    modified_file_name = file_name.replace(".wav", ".wav")

    # Create the modified file path
    modified_file_path = os.path.join(processed_folder, modified_file_name)

    # Save the modified audio as a new WAV file with the same parameters as the input
    sf.write(modified_file_path, modified_audio, sr, subtype='PCM_24')

    return modified_file_path

def pad_beginning(file_path, initial_duration, pre_roll):
    # Load the audio file
    audio, sr = sf.read(file_path)

    # Calculate the reduction duration
    reduction_initial = initial_duration - pre_roll

    # Check if initial silence duration is shorter
    if reduction_initial < 0:
        # Calculate the difference in length required to reach the pre-roll value
        diff_initial = pre_roll - initial_duration

        # Calculate the number of samples to add based on the difference in length
        add_samples_initial = int(diff_initial * sr)

        # Pad the beginning of the audio with zeros by adding the specified number of samples
        if audio.ndim > 1:
            initial_zeros = np.zeros((add_samples_initial, audio.shape[1]), dtype=audio.dtype)
        else:
            initial_zeros = np.zeros(add_samples_initial, dtype=audio.dtype)
        audio = np.concatenate((initial_zeros, audio), axis=0)

    # Create the processed folder path
    processed_folder = "./output/pad_beginning"
    os.makedirs(processed_folder, exist_ok=True)

    # Create a modified file name
    file_name = os.path.basename(file_path)
    modified_file_name = file_name.replace(".wav", ".wav")

    # Create the modified file path
    modified_file_path = os.path.join(processed_folder, modified_file_name)

    # Save the modified audio as a new WAV file with the same parameters as the input
    sf.write(modified_file_path, audio, sr, subtype='PCM_24')

    return modified_file_path


    # Load the audio file
    audio, sr = sf.read(file_path)

    # Calculate the reduction duration
    reduction_initial = initial_duration - pre_roll

    # Check if initial silence duration is shorter
    if reduction_initial < 0:
        # Calculate the difference in length required to reach the pre-roll value
        diff_initial = pre_roll - initial_duration

        # Calculate the number of samples to add based on the difference in length
        add_samples_initial = int(diff_initial * sr)

        # Pad the beginning of the audio with zeros by adding the specified number of samples
        if audio.ndim > 1:
            initial_zeros = np.zeros((add_samples_initial, audio.shape[1]), dtype=audio.dtype)
        else:
            initial_zeros = np.zeros(add_samples_initial, dtype=audio.dtype)
        audio = np.concatenate((initial_zeros, audio), axis=0)

    # Create the processed folder path
    processed_folder = "./output/pad_beginning"
    os.makedirs(processed_folder, exist_ok=True)

    # Create a modified file name
    file_name = os.path.basename(file_path)
    modified_file_name = file_name.replace(".wav", ".wav")

    # Create the modified file path
    modified_file_path = os.path.join(processed_folder, modified_file_name)

    # Save the modified audio as a new WAV file with the same parameters as the input
    sf.write(modified_file_path, audio, sr, subtype='PCM_24')

    return modified_file_path 

def pad_end(file_path, end_duration, pre_roll):
    # Load the audio file
    audio, sr = sf.read(file_path)

    # Calculate the reduction duration
    reduction_end = end_duration - pre_roll

    # Check if end silence duration is shorter
    if reduction_end < 0:
        # Calculate the difference in length required to reach the pre-roll value
        diff_end = pre_roll - end_duration

        # Calculate the number of samples to add based on the difference in length
        add_samples_end = int(diff_end * sr)

        # Pad the end of the audio with zeros by adding the specified number of samples
        if audio.ndim > 1:
            end_zeros = np.zeros((add_samples_end, audio.shape[1]), dtype=audio.dtype)
        else:
            end_zeros = np.zeros(add_samples_end, dtype=audio.dtype)
        audio = np.concatenate((audio, end_zeros), axis=0)

    # Create the processed folder path
    processed_folder = "./output/pad_end"
    os.makedirs(processed_folder, exist_ok=True)

    # Create a modified file name
    file_name = os.path.basename(file_path)
    modified_file_name = file_name.replace(".wav", ".wav")

    # Create the modified file path
    modified_file_path = os.path.join(processed_folder, modified_file_name)

    # Save the modified audio as a new WAV file with the same parameters as the input
    sf.write(modified_file_path, audio, sr, subtype='PCM_24')

    return modified_file_path

def calculate_initial_silence_duration(audio_file, db_threshold_start):
    # Load the audio file
    audio, sr = librosa.load(audio_file, mono=True)

    # Convert the dB threshold to amplitude scale
    amplitude_threshold = librosa.db_to_amplitude(db_threshold_start)

    # Calculate the peak value of the audio
    peak_value = audio.max()

    # Check if the peak value is below the threshold
    if peak_value < amplitude_threshold:
        # Calculate the duration of the audio
        audio_duration = len(audio) / sr

        return audio_duration

    # Find the start index where the audio exceeds the threshold
    start_index = (audio >= amplitude_threshold).argmax()

    # Calculate the initial silence duration before the speech
    silence_duration = start_index / sr

    return silence_duration

def calculate_end_silence_duration(audio_file, db_threshold_end):
    # Load the audio file
    audio, sr = librosa.load(audio_file, mono=True)

    # Reverse the audio signal
    reversed_audio = audio[::-1]

    # Convert the dB threshold to amplitude scale
    amplitude_threshold = librosa.db_to_amplitude(db_threshold_end)

    # Find the start index where the reversed audio exceeds the threshold
    start_index = (reversed_audio >= amplitude_threshold).argmax()

    # Calculate the end silence duration
    end_silence_duration = start_index / sr

    return end_silence_duration

def mix_audio_with_noise(audio_path, noise_path):
    audio = AudioSegment.from_file(audio_path)
    noise = AudioSegment.from_file(noise_path)

    # Make sure the audio and noise have the same duration
    audio = audio[:len(noise)]

    # Mix (add) the audio and noise together
    mixed_audio = audio.overlay(noise)

    return mixed_audio

def process_audio_files(noise_folder_path):
    audio_files = os.listdir(noise_folder_path)
    noise_folder = "./noise"
    processed_folder = "./output/added_noise"

    os.makedirs(processed_folder, exist_ok=True)

    # Get the list of noise files
    noise_files = os.listdir(noise_folder)

    for file_name in audio_files:
        audio_path = os.path.join(noise_folder_path, file_name)

        # Select a random noise file
        noise_file = random.choice(noise_files)
        noise_path = os.path.join(noise_folder, noise_file)

        # Read the audio file without converting it
        audio, audio_sr = sf.read(audio_path)

        # Read the noise file
        noise, noise_sr = sf.read(noise_path)

        # Check if audio and noise have the same sample rate
        if audio_sr != noise_sr:
            raise ValueError("Audio and noise have different sample rates.")

        # Make sure the noise is longer than the audio
        if len(noise) <= len(audio):
            raise ValueError("Noise duration should be longer than audio duration.")

        # Trim the noise to match the duration of the audio
        noise = noise[:len(audio)]

        # Mix (add) the audio and noise together
        mixed_audio = audio + noise

        # Save the mixed audio file in the processed folder with the original name
        processed_file_path = os.path.join(processed_folder, file_name)
        sf.write(processed_file_path, mixed_audio, audio_sr, 'PCM_24')
        st.write(f"Processed file: {file_name}")


    # Get a list of all subdirectories within the folder
    subdirectories = [f for f in os.listdir(noise_folder_path) if os.path.isdir(os.path.join(noise_folder_path, f))]
    
    # Delete each subdirectory within the folder
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(folder_path, subdirectory)
        shutil.rmtree(subdirectory_path)

def clean_temp_files(folder_path):
    # Remove all files
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

    # Remove all subfolders
    subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
    for subfolder in subfolders:
        shutil.rmtree(subfolder)
        print(f"Deleted folder: {subfolder}")

def move_files(source_folder, destination_folder):
                
    # Check if the source folder exists
    if not os.path.exists(source_folder):
        raise ValueError("Source folder does not exist!")

    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)

    # Copy and replace the files from the source folder to the destination folder
    files = os.listdir(source_folder)
    for file_name in files:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)
        shutil.copy2(source_path, destination_path)

    print("Files saved successfully!")


