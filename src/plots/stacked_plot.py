import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.plots.base_plot import MultipleRecordingPlot

class StackedPlot(MultipleRecordingPlot):
    def make_plot(self) -> None:
        n = len(self.walking_recordings)

        fig = make_subplots(rows=n,
                            cols=2,
                            shared_yaxes=True,
                            horizontal_spacing=0,
                            column_widths=[0.8, 0.2],
                            x_title="Time (s)",
                            y_title="Acceleration (g)",
                )

        for i, walking_recording in enumerate(self.walking_recordings):
            name = walking_recording.identifier
            df = walking_recording.df
            fig.add_trace(
                go.Scatter(
                    x=df["time (s)"],
                    y=df["acceleration (g)"],
                    mode='lines',
                    name=name,
                    line={"color" : self.color_scheme[name]},
                    legendgroup=name
                    ),
                row=i+1,
                col=1,
                )
            fig.add_trace(
                go.Violin(
                    y=df["acceleration (g)"],
                    name=name,
                    box_visible=True,
                    meanline_visible=True,
                    line={"color" : self.color_scheme[name]},
                    legendgroup=name,
                    showlegend=False,
                    ),
                row=i+1,
                col=2)
        fig.update_layout(hovermode="x", title_text="Accélération en fonction du temps")

        self.cache_plot = fig
