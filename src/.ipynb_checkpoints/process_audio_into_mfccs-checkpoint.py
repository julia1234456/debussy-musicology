# Clay Foye
# 
# Given source and target directories, process the .mp3 files from source directory into 
# MFCCs and store those in the target directory.

import os 
import sys
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from src.extract_mfcc import extract_mfcc, extract_mfcc_splits

"""
Examples / Usage
To process debussy recordings:
    python scripts/process_audio_into_mfccs.py data/debussy/recordings/ data/debussy/mfccs/

To process gamelan recordings:
    python scripts/process_audio_into_mfccs.py data/gamelan/recordings/ data/gamelan/mfccs/

"""



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_audio_into_mfccs.py <source_directory> <target_directory>")
        sys.exit(1)

    print("saving . .. ")

    source_directory = sys.argv[1]
    target_directory = sys.argv[2]

    if not os.path.exists(source_directory):
        print(f"Error: Source directory '{source_directory}' does not exist.")
        sys.exit(1)

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for root, _, files in os.walk(source_directory):
        for file in files:
            if file.endswith(".mp3"):
                source_file_path = os.path.join(root, file)
                target_file_path = os.path.join(
                    target_directory, os.path.splitext(file)[0] + ".npy"
                )

                if os.path.exists(target_file_path):
                    print(f"Skipping {source_file_path}, target file already exists.")
                    continue

                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)

                print(f"Processing {source_file_path} into {target_file_path}...")
                try:
                    # mfcc_features = extract_mfcc(source_file_path, target_num_frames=1000)
                    mfcc_features = extract_mfcc_splits(source_file_path)
                    np.save(target_file_path, mfcc_features)
                except Exception as e:
                    print(f"Failed to process {source_file_path}: {e}")