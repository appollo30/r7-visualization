from src.plots.base_plot import Plot
import plotly.graph_objects as go
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

class FrequencyPlot(Plot):
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
    
    