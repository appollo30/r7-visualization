import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class MovementData:
    COLORS = px.colors.qualitative.Plotly
    
    def __init__(self, dfs, names):
        if len(dfs) != len(names):
            raise ValueError("The number of dataframes and names must be the same")
        self.dfs = dfs
        self.names = names
        self.color_dict = {name: color for name, color in zip(self.names, MovementData.COLORS)}

    def multi_line_plot(self):
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
        fig.update_layout(hovermode="x")
        fig.update_xaxes(title_text="Time (s)")
        fig.update_yaxes(title_text="Acceleration (g)")
        return fig

    def violin_plots(self):
        fig = go.Figure()
        
        for df,name in zip(self.dfs,self.names):
            fig.add_trace(
                go.Violin(
                    y=df["acceleration (g)"],
                    name=name,
                    box_visible=True,
                    meanline_visible=True,
                    line={"color" : self.color_dict[name]}
                    ),
                )
        fig.update_yaxes(title_text="Time (s)")
        return fig

    def xyz_plot(self):
        fig = make_subplots(
            rows=3,
            cols=1,
            shared_xaxes=True,
            subplot_titles=["X", "Y", "Z"],
            x_title="Time (s)",
            y_title="Acceleration (g)"
            )
        
        for df,name in zip(self.dfs,self.names):
            fig.add_trace(
                go.Scatter(x=df["time (s)"],
                        y=df["X (g)"],
                        mode='lines',
                        name=name,
                        legendgroup=name,
                        line={"color" : self.color_dict[name]}
                        ),
                row=1,
                col=1)
            fig.add_trace(
                go.Scatter(x=df["time (s)"],
                        y=df["Y (g)"],
                        mode='lines',
                        name=name,
                        legendgroup=name,
                        line={"color" : self.color_dict[name]},
                        showlegend=False
                        ),
                row=2, col=1)
            fig.add_trace(
                go.Scatter(
                    x=df["time (s)"],
                    y=df["Z (g)"],
                    mode='lines',
                    name=name,
                    legendgroup=name,
                    line={"color" : self.color_dict[name]},
                    showlegend=False
                    ),
                row=3,
                col=1
                )
        fig.update_layout(hovermode="x")
        return fig

    def stacked_plot(self):
        n = len(self.names)
        
        fig = make_subplots(rows=n,
                            cols=2,
                            shared_yaxes=True,
                            horizontal_spacing=0,
                            column_widths=[0.8, 0.2],
                            x_title="Time (s)",
                            y_title="Acceleration (g)",
                )
        
        for i, (df,name) in enumerate(zip(self.dfs,self.names)):
            fig.add_trace(
                go.Scatter(
                    x=df["time (s)"],
                    y=df["acceleration (g)"],
                    mode='lines',
                    name=name,
                    line={"color" : self.color_dict[name]},
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
                    line={"color" : self.color_dict[name]},
                    legendgroup=name,
                    showlegend=False,
                    ), 
                row=i+1, 
                col=2)
        fig.update_layout(hovermode="x")
        
        return fig

    def make_all_plots(self):
        if len(self.names) == 0:
            return {}
        
        result = {
            "Line" : self.multi_line_plot(),
            "Violin" : self.violin_plots(),
            "Stacked" : self.stacked_plot(),
            "XYZ" : self.xyz_plot()
        }
        return result