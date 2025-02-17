from .base_plot import Plot
import plotly.graph_objects as go

class LinePlot(Plot):
    def create_plot(self) -> go.Figure:
        fig = go.Figure()

        for df,name in zip(self.dfs,self.names):
            fig.add_trace(
                go.Scatter(
                    x=df["time (s)"],
                    y=df["acceleration (g)"],
                    name=name,
                    line={"color" : self.color_dict[name]}
                    )
                )
        fig.update_layout(hovermode="x unified", title_text="Accélération en fonction du temps")
        fig.update_xaxes(title_text="Time (s)")
        fig.update_yaxes(title_text="Acceleration (g)")
        return fig