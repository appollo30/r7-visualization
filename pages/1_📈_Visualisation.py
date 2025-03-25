from typing import List, Dict, Optional
import streamlit as st
import plotly.graph_objects as go
from src.plot_factory import PlotFactory
from src.file_utils import get_all_file_names, get_specific_file
from src.file_uploader import handle_file_uploader

def handle_multiselect(all_files : List[str]) -> Optional[Dict[str,go.Figure]]:
    multiselect = st.multiselect(
        "Choisissez les fichiers à analyser",
        all_files,
        default=None,
        placeholder="Veuillez sélectionner des fichiers à analyser",
        max_selections=7
    )
    recordings = [get_specific_file(f) for f in multiselect]
    return recordings

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
    
    walking_recordings_from_database = handle_multiselect(all_files)
    walking_recordings_external = handle_file_uploader()
    all_walking_recordings = walking_recordings_from_database + walking_recordings_external
    
    markdown_text = "**Fichiers ajoutés**"
    for recording in all_walking_recordings:
        markdown_text += f"\n- {recording.name}/{recording.file_name}"
    st.markdown(markdown_text)
    
    if len(all_walking_recordings) > 0:
        plot_factory = PlotFactory(all_walking_recordings)
        plot_dict = plot_factory.get_all_plots()
        handle_plots_and_selectbox(plot_dict)

main()
