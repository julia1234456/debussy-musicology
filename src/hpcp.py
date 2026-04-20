import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


def compute_hpcp(y, sr, n_octaves=7, bins_per_octave=12,tuning=0,norm=False):
    """
    Compute the Harmonic Pitch Class Profile (HPCP) of an audio signal.

    Uses a Constant-Q Transform (CQT) as the spectral backbone, then folds
    the energy into chroma bins. Optionally normalizes the resulting vector
    so that bin values sum to 1 (useful for cross-recording comparisons).
    """
    n_bins = n_octaves * bins_per_octave 
    
    q_transform = np.abs(librosa.cqt(y, sr=sr, n_bins=n_bins, bins_per_octave=bins_per_octave))
    #q_transform = np.abs(librosa.stft(y))
    chroma = librosa.feature.chroma_cqt(C=q_transform, sr=sr, tuning=tuning, bins_per_octave=bins_per_octave, n_chroma=bins_per_octave)
    hpcp_vector = np.mean(chroma, axis=1)

    if norm: 
        hpcp_vector = hpcp_vector / np.sum(hpcp_vector) 

    return chroma, hpcp_vector

def compute_all_hpcp(filenames, bins_per_octave=120, genre='debussy'): 
    """
    Batch-compute normalized HPCP vectors for a list of recordings.
    Loads each file from 'data/recordings_{genre}/', applies tuning correction,
    and computes a high-resolution HPCP. 
    """
    hpcps = []
    for filename in filenames: 
        try: 
            print(f'Compute HPCP {filename}')

            y, sr, tuning_deviation = load_and_process(f'data/recordings_{genre}/{filename}.mp3')
            chrom, hpcp = compute_hpcp(y, sr, n_octaves=7, bins_per_octave=bins_per_octave, tuning=tuning_deviation, norm=True)
            hpcps.append(hpcp)
        except Exception: 
            print(f'Skip {filename}')
    return hpcps

def display_chroma(chroma, sr, title='Chroma Representation'):
    """
    Display a chroma-gram as a colour-mapped time-frequency image.

    Y-axis tick labels are hidden by default and shown every 10 bins to avoid
    clutter when using high-resolution (e.g. 120-bin) chroma.
    """
    plt.figure(figsize=(10, 4))
    plot =librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', sr=sr)
   
    plt.setp(plot.axes.get_yticklabels(), visible=False)  
    plt.setp(plot.axes.get_yticklabels()[::10], visible=True)
    plt.colorbar()
    plt.title(f'{title}')
    plt.tight_layout()
    plt.show()

def display_hpcp(hpcp_vector, title= 'HPCP Vector', nb_bins=12): 
    """
    Display an HPCP vector as a bar chart with pitch-class labels on the x-axis.

    Supports two resolution modes:
      - 12 bins  : one bar per semitone, corresponding to the occidental scale.
      - 120 bins : one bar per 1/10-semitone, allowing to capture non-occidental scale.

    """
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 
              'F#', 'G', 'G#', 'A', 'A#', 'B']
    r= [ i for i in range(hpcp_vector.shape[0])]
    plot =plt.bar(r, hpcp_vector)
    if nb_bins==12:
        plt.xticks(range(12), note_names)
    
    if nb_bins==120: 
        tick_locs = [i * 10 for i in range(12)]  
        tick_labels = note_names 
        plt.xticks(tick_locs, tick_labels)
    

    plt.title(f'{title}')
    plt.xlabel('Classes')
    plt.ylabel('HPCP')
    plt.show()
    
    
def load_and_process(path, duration=None, bins_per_octave=120): 
    """
    Load an audio file, trim silence, and estimate its tuning deviation.

    Uses a reassigned spectrogram to obtain precise instantaneous frequency
    estimates, which are then fed to librosa's pitch tuning estimator.
    """
    y, sr = librosa.load(path, duration=duration)
    y, _ = librosa.effects.trim(y)
    freqs, times, mags = librosa.reassigned_spectrogram(y, sr=sr,fill_nan=True)
    tuning_deviation = librosa.pitch_tuning(freqs, bins_per_octave=bins_per_octave)
    return y, sr, tuning_deviation


def display_two_hpcp(hpcp1, hpcp2, label1='label1', label2='label2'): 
    """
    Display two HPCP vectors side by side as a grouped bar chart for comparison.

    Assumes 120-bin resolution (1/10-semitone); pitch-class labels are placed
    at every 10th bin. Useful for visually comparing the tonal profiles of two
    different recordings or pieces."""
    x = np.arange(120)
    width = 0.35

    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F',
                    'F#', 'G', 'G#', 'A', 'A#', 'B']

    plt.bar(x - width/2, hpcp1, width, label=label1)
    plt.bar(x + width/2, hpcp2, width, label=label2)
    tick_locs = [i * 10 for i in range(12)]  
    plt.xticks(tick_locs, pitch_classes)
    plt.title('Normalized HPCP Comparison')
    plt.xlabel('Pitch Class')
    plt.ylabel('Normalized Contribution')
    plt.legend()
    plt.tight_layout()
    plt.show()