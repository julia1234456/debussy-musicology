import numpy as np
import librosa
import matplotlib.pyplot as plt
import scipy

def extract_onset_from_band(band, sr,lag, aggregate=np.mean, max_size=None):
    """
    Extract onset strength from a band.
    """
    if max_size is not None:
        ref = scipy.ndimage.maximum_filter1d(band, max_size, axis=-2)
    else:
        ref = band
    onset_strength = band[..., lag:] - ref[..., :-lag]
    onset_strength = np.maximum(0.0, onset_strength)
    if aggregate is not None:
        onset_strength = aggregate(onset_strength, axis=0)
    return onset_strength

# # These parameter settings found by large-scale search
#         kwargs.setdefault("pre_max", 0.03 * sr // hop_length)  # 30ms
#         kwargs.setdefault("post_max", 0.00 * sr // hop_length + 1)  # 0ms
#         kwargs.setdefault("pre_avg", 0.10 * sr // hop_length)  # 100ms
#         kwargs.setdefault("post_avg", 0.10 * sr // hop_length + 1)  # 100ms
#         kwargs.setdefault("wait", 0.03 * sr // hop_length)  # 30ms
#         kwargs.setdefault("delta", 0.07)

def get_peak_pick_params(sr, max_bpm=300):
    """
    Get parameters for peak picking.
    """
    pre_max = 10
    post_max = 5
    pre_avg = 10
    post_avg = 3
    wait = 1
    delta = 0.01
    print(f"pre_max: {pre_max}, post_max: {post_max}, pre_avg: {pre_avg}, post_avg: {post_avg}, wait: {wait}, delta: {delta}")
    return pre_max, post_max, pre_avg, post_avg, wait, delta

def get_onset_peaks(onset_strength, sr, hop_length):
    """
    Get onset peaks from onset strength.
    """
    pre_max, post_max, pre_avg, post_avg, wait, delta = get_peak_pick_params(sr, hop_length)
    onset_peaks = librosa.util.peak_pick(onset_strength, pre_max=pre_max, post_max=post_max,
                                         pre_avg=pre_avg, post_avg=post_avg,
                                         delta=delta, wait=wait)
    peak_strengths = onset_strength[onset_peaks]
    return onset_peaks,peak_strengths

def filter_peaks(peak_strengths, peaks, onset_strength, threshold=0.5, wait=20):
    """
    Filter peaks based on a threshold.
    """
    mask = peak_strengths > onset_strength.mean() + threshold * onset_strength.std()
    filtered_peaks = peaks[mask]
    diff = np.diff(filtered_peaks)
    filtered_peaks = filtered_peaks[np.insert(diff > wait, 0, True)]
    filtered_peak_strengths = peak_strengths[mask]
    filtered_peak_strengths = filtered_peak_strengths[np.insert(diff > wait, 0, True)]
    return filtered_peaks, filtered_peak_strengths