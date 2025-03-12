from typing import List
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src.walking_recording import WalkingRecording

class Plot:
    COLORS = px.colors.qualitative.Plotly

    def __init__(self):
        self.cache_plot = None

    def make_plot(self) -> None:
        raise NotImplementedError("Make plot method not implemented")

    def get_plot(self) -> go.Figure:
        if self.cache_plot is None:
            self.make_plot()
        return self.cache_plot

    def show(self):
        _ = self.get_plot()
        st.plotly_chart(self.cache_plot)

class SingleRecordingPlot(Plot):
    def __init__(self, walking_recording : WalkingRecording):
        super().__init__()
        self.walking_recording = walking_recording

    def make_plot(self) -> None:
        raise NotImplementedError("Make plot method not implemented")

class MultipleRecordingPlot(Plot):
    def __init__(self, walking_recordings : List[WalkingRecording]):
        super().__init__()
        self.walking_recordings = walking_recordings
        names = [walking_recording.name for walking_recording in walking_recordings]
        names_counter = {name : names.count(name) for name in names}
        for walking_recording in walking_recordings:
            if names_counter[walking_recording.name] > 1:
                walking_recording.identifier = f"{walking_recording.name} ({walking_recording.file_name})"
            else:
                walking_recording.identifier = walking_recording.name
        self.color_scheme = {walking_recording.identifier : color for walking_recording, color in zip(self.walking_recordings, Plot.COLORS)}

    def make_plot(self) -> None:
        raise NotImplementedError("Make plot method not implemented")
