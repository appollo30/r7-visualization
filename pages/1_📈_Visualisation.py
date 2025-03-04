from typing import List
import streamlit as st
from src.walking_data import WalkingData
from src.walking_recording import WalkingRecording
from src.utils import get_all_files 
   
def handle_multiselect(all_files : List[str]) -> List[WalkingRecording]:
    multiselect = st.multiselect(
        "Choisissez les fichiers à analyser",
        all_files,
        default=None,
        placeholder="Veuillez sélectionner des fichiers à analyser",
        max_selections=6
    )
    recordings = [WalkingRecording.from_csv(f"data/processed/{f}") for f in multiselect]
    walking_data = WalkingData(recordings)
    return walking_data

def handle_plots_and_selectbox(walking_data : WalkingData) -> None:
    plot_names = walking_data.get_plot_names()
    with st.container():
        if not walking_data.is_empty():
            segmented_control = st.segmented_control(
                label="Type de graphe :",
                options=plot_names,
                selection_mode="single",
                default="Line"
            )
            if segmented_control:
                walking_data.cache_plots[segmented_control].show()

def main():
    st.set_page_config(page_title="Visualisation", page_icon="📈", layout="wide")
    st.title("Visualisation des données de démarche")
    all_files = get_all_files()
    walking_data = handle_multiselect(all_files)
    walking_data.make_all_plots()
    handle_plots_and_selectbox(walking_data)

main()
