import argparse
import os
import pytubefix
import ffmpeg
import pandas as pd
import tqdm

DCMLAB_GIT_URL = "git@github.com:DCMLab/debussy_piano.git" # DCMLab Debussy piano dataset repository
REC_SOURCES_CSV_PATH = "../data/data_sources.csv" # CSV listing YouTube recording URLs and metadata
RAW_DATA_PATH = "../data/raw"

def download_deb_piano(git_url, data_dir):
    """Clone the DCMLab Debussy piano dataset (scores, annotations) from GitHub."""
    os.system(f"git clone --recursive {git_url} {data_dir}")

def download_yt_recordings(list_urls, filenames, data_dir, format="wav"):
    """Download a list of YouTube recordings and save them to disk."""
    for url, filename in tqdm.tqdm(zip(list_urls, filenames), total=len(min(list_urls, filenames))):
        download_recording(url, f"{data_dir}/{filename}", format)

def download_deb_midi():
    pass

def download_recording(url, filename, format="wav"):
    """Download a single YouTube video as an audio file using ffmpeg."""
    if format == 'mp3':
        audio_opts = {
            'acodec': 'libmp3lame',
            'audio_bitrate': '192k',
            'ac': 2
        }
    elif format == 'wav':
        audio_opts = {
            'acodec': 'pcm_s16le',  # standard WAV codec
            'ac': 2,
            'ar': 44100             # optional: sample rate
        }
    yt = pytubefix.YouTube(url)
    stream = yt.streams[0].url  # Get the first available stream (usually audio)

    ffmpeg.input(stream)\
        .output(f"{filename}.{format}", loglevel="error", **audio_opts)\
        .overwrite_output()\
        .run()

def load_recording_sources(csv_path):
    """Load the recordings metadata CSV into a DataFrame."""
    df = pd.read_csv(csv_path)
    return df

def get_filenames_and_urls(source_df, skip_cuts=True):
    """ Extract valid recording URLs and their corresponding output filenames from the metadata DataFrame."""
    mask = source_df["recording_url"].notna()

    if skip_cuts:
        # remove recordings that need to be cut up for now
        mask = mask & source_df["start_time"].isna() & source_df["end_time"].isna()
    df = source_df[mask]
    df["piece"] = df["piece"].map(lambda x: x.lower().replace(" ", "_"))
    return list(df.recording_url), list(df.piece)

def download_data_raw(data_path, rec_sources_path=None, format="mp3"):
    """
    Downloads debussy_piano, and if a rec_source_path is specified also downloads all recordings.
    Format can either be mp3 or wav 
    """
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    
    download_deb_piano(DCMLAB_GIT_URL, data_path)
    download_deb_midi() # TODO

    if rec_sources_path:
        rec_path = f"{data_path}/recordings"
        if not os.path.exists(rec_path):
            os.makedirs(rec_path)
        urls, filenames = get_filenames_and_urls(load_recording_sources(rec_sources_path))
        download_yt_recordings(urls, filenames, rec_path, format)
        download_yt_recordings()


def main():
    download_data_raw(RAW_DATA_PATH, REC_SOURCES_CSV_PATH, format="mp3")

if __name__ == "__main__":
    main()

