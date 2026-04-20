import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt


def compute_hpcp(y, sr, n_octaves=7, bins_per_octave=12,tuning=0):
    n_bins = n_octaves * bins_per_octave 
    
    q_transform = np.abs(librosa.cqt(y, sr=sr, n_bins=n_bins, bins_per_octave=bins_per_octave))
    chroma = librosa.feature.chroma_cqt(C=q_transform, sr=sr, tuning=tuning, bins_per_octave=bins_per_octave, n_chroma=bins_per_octave)
    hpcp_vector = np.mean(chroma, axis=1)

    return chroma, hpcp_vector

def display_chroma(chroma, sr, title='Chroma Representation'):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', sr=sr)
    plt.colorbar()
    plt.title(f'{title}')
    plt.tight_layout()
    plt.show()

def display_hpcp(hpcp_vector, title= 'HPCP Vector'): 
    r= [ i for i in range(hpcp_vector.shape[0])]
    plt.bar(r, hpcp_vector)
    plt.title(f'{title}')
    plt.xlabel('Classes')
    plt.ylabel('HPCP')
    plt.show()
    
    


