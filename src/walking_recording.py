from dataclasses import dataclass
import os
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
from scipy.signal import correlate
import pandas as pd
import numpy as np

@dataclass
class WalkingRecording:
    """
    Class to handle movement data, one recording contains one df, a name and a file name (optional)
    """
    df : pd.DataFrame
    name : str
    file_name : str | None = None
    cache_fft = None
    cache_steps = None
    identifier = None

    @classmethod
    def from_csv(cls,file_path):
        return cls(
            pd.read_csv(file_path),
            os.path.basename(os.path.dirname(file_path)),
            os.path.basename(file_path)
            )

    def get_recording_length(self) -> float:
        return self.df["time (s)"].iloc[-1] - self.df["time (s)"].iloc[0]

    def get_sampling_period(self) -> float:
        return self.df["time (s)"].diff().mean()

    def get_fft(self):
        if self.cache_fft is not None:
            return self.cache_fft
        N = len(self.df["time (s)"])
        T = self.df["time (s)"].iloc[-1] / N
        yf = fft(self.df["acceleration (g)"])
        xf = fftfreq(N, T)[:N//2]
        self.cache_fft = yf[:N//2], xf
        return self.cache_fft

    def get_steps(self) -> np.ndarray:
        if self.cache_steps is not None:
            return self.cache_steps
        self.cache_steps = find_peaks(self.df['acceleration (g)'],
                                      height=1.1,
                                      prominence=0.2,
                                      distance=30
                                      )[0]
        return self.cache_steps

    def get_autocorrelation(self):
        X_normalized = (self.df['acceleration (g)'] - self.df['acceleration (g)'].mean()) / self.df['acceleration (g)'].std()
        return correlate(X_normalized, X_normalized[::-1], mode='full')

    def get_frequency_from_fft(self) -> float:
        X, freqs = self.get_fft()
        N = len(X)
        return freqs[1:N//2][np.argmax(np.abs(X[1:N//2]))]

    def get_frequency_from_counting_steps(self) -> float:
        steps = self.get_steps()
        period = self.df["time (s)"].iloc[steps].diff().mean()
        return 1/period

    def get_step_duration_std(self) -> float:
        steps = self.get_steps()
        duration = self.df["time (s)"].iloc[steps].diff()
        return duration.std()

    def get_acceleration_amplitude(self) -> float:
        return self.df["acceleration (g)"].max() - self.df["acceleration (g)"].min()

    def get_std(self,field):
        return self.df[field].std()

    def __str__(self) -> str:
        return f"""WalkingRecording(name = \"{self.name}\",file_name = \"{self.file_name}\")
    - Sampling frequency = {1/self.get_sampling_period():.2f} Hz
    - Recording length = {self.get_recording_length():.2f} s"""

    def __repr__(self) -> str:
        return str(self)
