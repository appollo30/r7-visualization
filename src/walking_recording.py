from dataclasses import dataclass
import pandas as pd
import os

@dataclass
class WalkingRecording:
    """
    Class to handle movement data, one recording contains one df, a name and a file name (optional)
    """
    df : pd.DataFrame
    name : str
    file_name : str | None = None
    
    @classmethod
    def from_csv(cls,file_path):
        return cls(
            pd.read_csv(file_path),
            os.path.basename(os.path.dirname(file_path)),
            os.path.basename(file_path)
            )
    
    def get_recording_length(self) -> float:
        return self.df["time (s)"].iloc[-1] - self.df["time (s)"].iloc[0]
    
    def get_sampling_frequency(self) -> float:
        return self.df["time (s)"].diff().mean()
    
    def __str__(self) -> str:
        return f"""WalkingRecording(name = \"{self.name}\",file_name = \"{self.file_name}\")
    - Sampling frequency = {self.get_sampling_frequency():.2f} Hz
    - Recording length = {self.get_recording_length():.2f} s"""
    
    def __repr__(self) -> str:
        return str(self)
    