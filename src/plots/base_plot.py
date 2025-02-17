import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List
import streamlit as st

class Plot:
    COLORS = px.colors.qualitative.Plotly
    
    def __init__(self, dfs: List[pd.DataFrame], names: List[str]):
        self.dfs = dfs
        self.names = names
        self.color_dict = dict(zip(self.names, Plot.COLORS))
        self.cache_plot = None
    
    def show(self):
        raise NotImplementedError("Show method not implemented")
    
class SinglePlot(Plot):
    def make_plot(self) -> None:
        raise NotImplementedError("Create plot method not implemented")
    
    def show(self) -> None:
        if self.cache_plot is None:
            self.make_plot()
        st.plotly_chart(self.cache_plot)