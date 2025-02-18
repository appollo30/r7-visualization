from src.plots.base_plot import SinglePlot
import plotly.graph_objects as go
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
import numpy as np
import streamlit as st

class FrequencyPlot(SinglePlot):
    def __init__(self, dfs, names):
        super().__init__(dfs, names)
    
    def fft(self):
        ffts = []
        freqs = []
        for df in self.dfs:
            N = len(df["time (s)"])
            T = df["time (s)"].iloc[-1] / N
            yf = fft(df["acceleration (g)"])
            xf = fftfreq(N, T)[:N//2]
            ffts.append(yf[:N//2])
            freqs.append(xf)
        return ffts, freqs
    
    def make_plot(self):
        N = len(self.dfs[0]["time (s)"])
        ffts, freqs = self.fft()
        fig = go.Figure()
        for i, (fft, freq) in enumerate(zip(ffts, freqs)):
            fig.add_trace(
                go.Scatter(
                    x=freq,
                    y=2.0/N * np.abs(fft),
                    mode='lines',
                    name=self.names[i],
                    line={"color" : self.color_dict[self.names[i]]}
                    )
                )
        fig.update_layout(
            title='Transformée de Fourier',
            xaxis_title='Fréquence (Hz)',
            yaxis_title='Amplitude (g)',
            hovermode = "x"
        )
        fig.update_xaxes(range=[0, 3])
        self.cache_plot = fig
    
    