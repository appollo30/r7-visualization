import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import List
from src.walking_recording import WalkingRecording

class Plot:
    COLORS = px.colors.qualitative.Plotly
    
    def __init__(self):
        self.cache_plot = None
    
    def make_plot(self) -> None:
        raise NotImplementedError("Make plot method not implemented")
    
    def get_plot(self) -> go.Figure:
        if not self.cache_plot:
            self.make_plot()
        return self.cache_plot
    
    def show(self):
        cache_plot = self.get_plot()
        st.plotly_chart(self.cache_plot)
    
class SingleRecordingPlot(Plot):
    def __init__(self, walking_recording : WalkingRecording):
        super().__init__()
        self.walking_recording = walking_recording
        
    
class MultipleRecordingPlot(Plot):
    def __init__(self, walking_recordings : List[WalkingRecording]):
        super().__init__()
        self.walking_recordings = walking_recordings
        self.color_scheme = {walking_recording.name : color for walking_recording, color in zip(self.walking_recordings, Plot.COLORS)}
