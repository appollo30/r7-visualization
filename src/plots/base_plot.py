import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List

class Plot:
    COLORS = px.colors.qualitative.Plotly
    
    def __init__(self, dfs: List[pd.DataFrame], names: List[str]):
        self.dfs = dfs
        self.names = names
        self.color_dict = dict(zip(self.names, Plot.COLORS))
    
    def create_plot(self) -> go.Figure:
        raise NotImplementedError("This method must be implemented in the child class")
    
    def show(self):
        fig = self.create_plot()
        fig.show()