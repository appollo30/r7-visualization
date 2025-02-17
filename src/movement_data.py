from src.plots.line_plot import LinePlot
from src.plots.violin_plot import ViolinPlot
from src.plots.stacked_plot import StackedPlot
from src.plots.xyz_plot import XYZPlot

class MovementData:
    """
    Class to handle movement data
    """
    plot_classes = {
        "Line" : LinePlot,
        "Violin" : ViolinPlot,
        "Stacked" : StackedPlot,
        "XYZ" : XYZPlot
    }
    
    def __init__(self, dfs, names):
        if len(dfs) != len(names):
            raise ValueError("The number of dataframes and names must be the same")
        self.dfs = dfs
        self.names = names

    def make_plot(self,plot_name):
        if plot_name not in self.plot_classes:
            raise ValueError(f"Plot {plot_name} not found")
        return self.plot_classes[plot_name](self.dfs,self.names).create_plot()
    
    def make_all_plots(self):
        if len(self.names) == 0:
            return {}

        result = {plot_name : self.make_plot(plot_name) for plot_name in self.plot_classes.keys()}
        
        return result
