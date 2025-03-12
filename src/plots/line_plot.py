import plotly.graph_objects as go
from src.plots.base_plot import MultipleRecordingPlot

class LinePlot(MultipleRecordingPlot):
    def make_plot(self) -> None:
        fig = go.Figure()

        for walking_recording in self.walking_recordings:
            name = walking_recording.identifier
            df = walking_recording.df
            fig.add_trace(
                go.Scatter(
                    x=df["time (s)"],
                    y=df["acceleration (g)"],
                    name=name,
                    line={"color" : self.color_scheme[name]}
                    )
                )
        fig.update_layout(hovermode="x unified", title_text="Accélération en fonction du temps")
        fig.update_xaxes(title_text="Time (s)")
        fig.update_yaxes(title_text="Acceleration (g)")
        self.cache_plot = fig
