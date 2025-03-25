import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import streamlit as st
import pandas as pd
from src.plots.base_plot import MultipleRecordingPlot

class FrequencyPlot(MultipleRecordingPlot):
    def stacked_fft_plot(self):
        n = len(self.walking_recordings)
        fig = make_subplots(rows=n,cols=1)
        for i, walking_recording in enumerate(self.walking_recordings):
            name = walking_recording.identifier
            fft, freq = walking_recording.get_fft()
            fig.add_trace(
                go.Scatter(
                    x=freq,
                    y=2.0/n * np.abs(fft),
                    mode='lines',
                    name=name,
                    line={"color" : self.color_scheme[name]},
                    legendgroup=name,
                    ),
                row=i+1,
                col=1,
                )
        fig.update_layout(
            title='Transformée de Fourier',
            xaxis_title='Fréquence (Hz)',
            yaxis_title='Amplitude (g)',
            hovermode = "x"
        )
        fig.update_xaxes(range=[0, 3])
        return fig

    def superimposed_fft_plot(self):
        fig = go.Figure()
        for walking_recording in self.walking_recordings:
            name = walking_recording.identifier
            fft, freq = walking_recording.get_fft()
            fig.add_trace(
                go.Scatter(
                    x=freq,
                    y=2.0/len(self.walking_recordings) * np.abs(fft),
                    mode='lines',
                    name=name,
                    line={"color" : self.color_scheme[name]},
                    legendgroup=name,
                    showlegend=False
                )
            )
        fig.update_layout(
            title='Transformée de Fourier',
            xaxis_title='Fréquence (Hz)',
            yaxis_title='Amplitude (g)',
            hovermode = "x"
        )
        fig.update_xaxes(range=[0, 3])
        return fig

    def steps_plot(self):
        n = len(self.walking_recordings)
        fig = make_subplots(rows=n,cols=1)
        for i, walking_recording in enumerate(self.walking_recordings):
            name = walking_recording.identifier
            df = walking_recording.df
            steps = walking_recording.get_steps()
            fig.add_trace(
                go.Scatter(
                    x=df['time (s)'],
                    y=df['acceleration (g)'],
                    mode='lines',
                    name=name,
                    line={"color" : self.color_scheme[name]},
                    legendgroup=name,
                    showlegend=False
                ),
                row=i+1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=df['time (s)'].iloc[steps],
                    y=df['acceleration (g)'].iloc[steps],
                    mode='markers',
                    name='Pas détéctés',
                    line={"color" : "#FD3216"},
                    legendgroup="Pas détéctés",
                    showlegend=(i==0)
                ),
                row=i+1,
                col=1,
            )
        fig.update_layout(
            title='Détection des pas',
            xaxis_title='Temps (s)',
            yaxis_title='Accélération (g)'
        )
        return fig

    def get_metrics_df(self,needs_identifier=True):
        metrics = []
        for walking_recording in self.walking_recordings:
            if needs_identifier:
                name = walking_recording.identifier
            else:
                name = walking_recording.name
            steps = walking_recording.get_steps()
            file_name = walking_recording.file_name
            metrics.append(
                {
                    "Nom": name,
                    "Fichier source": file_name,
                    "Longueur de l'enregistrement (s)": walking_recording.get_recording_length(),
                    "Nombre de pas": len(steps),
                    "Fréquence des pas par fft (Hz)": walking_recording.get_frequency_from_fft(),
                    "Fréquence des pas par comptage (Hz)": walking_recording.get_frequency_from_counting_steps(),
                    "Ecart-type de la durée des pas (s)" : walking_recording.get_step_duration_std(),
                    "Amplitude de l'accélération (g)": walking_recording.get_acceleration_amplitude(),
                }
            )
        metrics_df = pd.DataFrame(metrics)
        metrics_df["Longueur de l'enregistrement (s)"] = metrics_df["Longueur de l'enregistrement (s)"].round(2)
        return metrics_df

    def make_plot(self):
        n = len(self.walking_recordings)
        specs = [[{"type": "scatter"},{"type": "scatter"}]] * n
        specs.append([{"type": "scatter","colspan": 2}, None])
        heights = [1]*n + [2]
        titles = [""]*2*n + ["Superposition des transformées de Fourier"]
        fig = make_subplots(
            rows=n+1,
            cols=2,
            column_titles=["Détection des pas","Transformée de Fourier"],
            row_titles=[walking_recording.name for walking_recording in self.walking_recordings],
            shared_xaxes=True,
            column_widths=[0.7,0.3],
            row_heights=heights,
            specs=specs,
            subplot_titles=titles,
            vertical_spacing=0.05,
        )
        steps = self.steps_plot()
        stacked_fft = self.stacked_fft_plot()
        superimposed_fft = self.superimposed_fft_plot()

        for i, walking_recording in enumerate(self.walking_recordings):
            fig.add_trace(steps.data[2*i], row=i+1, col=1)
            fig.add_trace(steps.data[2*i+1], row=i+1, col=1)
            fig.add_trace(stacked_fft.data[i], row=i+1, col=2)
            fig.update_yaxes(range=[0.2, 1.8], row=i+1, col=1)
            fig.update_xaxes(range=[0, 3], row=i+1, col=2)
            fig.add_trace(superimposed_fft.data[i], row=n+1, col=1)
            fig.update_xaxes(range=[0, 3], row=n+1, col=1)

        fig.update_layout(
            title="Analyse de la fréquence des pas",
            height=n*200 + 400,
        )

        self.cache_plot = fig

    def show(self):
        self.cache_plot = self.get_plot()
        st.table(self.get_metrics_df(needs_identifier=True))
        st.plotly_chart(self.cache_plot)
