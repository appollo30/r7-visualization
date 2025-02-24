from src.plots.line_plot import LinePlot
from src.plots.violin_plot import ViolinPlot
from src.plots.stacked_plot import StackedPlot
from src.plots.xyz_plot import XYZPlot
from src.plots.frequency_plot import FrequencyPlot
from src.walking_recording import WalkingRecording
from typing import List, Dict

class WalkingData:
    """
    Class to handle movement data
    """
    plot_classes = {
        "Line" : LinePlot,
        "Violin" : ViolinPlot,
        "Stacked" : StackedPlot,
        "XYZ" : XYZPlot,
        "Frequency" : FrequencyPlot
    }
    
    def __init__(self, walking_recordings : List[WalkingRecording]):
        self.walking_recordings = walking_recordings
        self.cache_plots = None

    def make_all_plots(self) -> Dict:
        self.cache_plots = {name: plot_class(self.walking_recordings) for name, plot_class in self.plot_classes.items()}
        
    def get_plot_names(self) -> List[str]:
        if len(self.walking_recordings) == 0:
            return []
        return list(self.plot_classes.keys())
    
    def is_empty(self) -> bool:
        return not bool(self.walking_recordings)
    
    def __str__(self) -> str:
        return "\n".join([str(walking_recording) for walking_recording in self.walking_recordings])
    
    def __repr__(self) -> str:
        return str(self)
