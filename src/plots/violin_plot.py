from src.plots.base_plot import MultipleRecordingPlot
import plotly.graph_objects as go

class ViolinPlot(MultipleRecordingPlot):
    def make_plot(self) -> None:
        fig = go.Figure()

        for walking_recording in self.walking_recordings:
            name = walking_recording.identifier
            df = walking_recording.df
            fig.add_trace(
                go.Violin(
                    y=df["acceleration (g)"],
                    name=name,
                    box_visible=True,
                    meanline_visible=True,
                    line={"color" : self.color_scheme[name]}
                    ),
                )
        fig.update_yaxes(title_text="Acceleration (g)")
        fig.update_layout(title_text="Distribution de l'accélération")
        self.cache_plot = fig