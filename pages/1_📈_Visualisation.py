from typing import List, Dict, Optional
import streamlit as st
import plotly.graph_objects as go
from src.plot_factory import PlotFactory
from src.walking_recording import WalkingRecording
from src.file_utils import get_all_file_names

def handle_multiselect(all_files : List[str]) -> Optional[Dict[str,go.Figure]]:
    multiselect = st.multiselect(
        "Choisissez les fichiers à analyser",
        all_files,
        default=None,
        placeholder="Veuillez sélectionner des fichiers à analyser",
        max_selections=7
    )
    if len(multiselect) == 0:
        return None
    recordings = [WalkingRecording.from_csv(f"data/processed/{f}") for f in multiselect]
    plot_factory = PlotFactory(recordings)
    plot_dict = plot_factory.get_all_plots()
    return plot_dict

def handle_plots_and_selectbox(plot_dict : Optional[Dict[str,go.Figure]]) -> None:
    if plot_dict is None:
        return
    with st.container():
        plot_names = list(plot_dict.keys())
        segmented_control = st.segmented_control(
            label="Type de graphe :",
            options=plot_names,
            selection_mode="single",
            default="Line"
        )
        if segmented_control:
            plot_dict[segmented_control].show()

def main():
    st.set_page_config(page_title="Visualisation", layout="wide")
    st.title("Visualisation des données de démarche")
    all_files = get_all_file_names()
    plot_dict = handle_multiselect(all_files)
    handle_plots_and_selectbox(plot_dict)

main()
