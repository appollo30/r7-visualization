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

    def make_all_plots(self):
        return {name: plot_class(self.dfs, self.names) for name, plot_class in self.plot_classes.items()}
        
    def get_plot_names(self):
        if len(self.names) == 0:
            return []
        return list(self.plot_classes.keys())
