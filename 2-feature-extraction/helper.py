import numpy as np
import seaborn as sns; sns.set()
from scipy import signal
from scipy.integrate import simps


# Define EEG bands
eeg_bands = {'delta': (0, 4),
             'theta': (4, 8),
             'alpha': (8, 13),
             'beta': (13, 30),
             'gamma': (30, 45)}

def relative_psd(x, fs, window, band):
    if band == 'delta':
        low, high = eeg_bands['delta'][0], eeg_bands['delta'][1]
    elif band == 'theta':
        low, high = eeg_bands['theta'][0], eeg_bands['theta'][1]
    elif band == 'alpha':
        low, high = eeg_bands['alpha'][0], eeg_bands['alpha'][1]
    elif band == 'beta':
        low, high = eeg_bands['beta'][0], eeg_bands['beta'][1]
    elif band == 'gamma':
        low, high = eeg_bands['gamma'][0], eeg_bands['gamma'][1]

    # Compute PSD using Welch's method
    freqs, psd = signal.welch(x, fs, nperseg=window)
    # Find frequencies that intersect with selected band
    idx_band = np.logical_and(freqs >= low, freqs <= high)
    # Calculate frequency resolution
    freq_res = freqs[1] - freqs[0]
    # Compute absolute band power
    band_power = simps(psd[idx_band], dx=freq_res)
    # Compute total power
    total_power = simps(psd, dx=freq_res)
    # # Calculate relative band power
    relative_band = 100 * (band_power / total_power)

    return relative_band