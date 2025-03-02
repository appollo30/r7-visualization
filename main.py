"""
Module main de l'application Streamlit
Pour le lancer : streamlit run main.py
"""
import glob
import os
from typing import List
import streamlit as st
from src.walking_data import WalkingData
from src.walking_recording import WalkingRecording
import random

@st.cache_data
def get_all_files() -> List[str]:
    random.seed(42)
    all_files = glob.glob("data/processed/*/*")
    all_files_no_prefix = [os.path.relpath(f, "data/processed") for f in all_files]
    random.shuffle(all_files_no_prefix)
    return all_files_no_prefix
    
def handle_multiselect(all_files : List[str]) -> List[WalkingRecording]:
    multiselect = st.multiselect(
        "Choisissez les fichiers à analyser",
        all_files,
        default=None,
        max_selections=6
    )
    recordings = [WalkingRecording.from_csv(f"data/processed/{f}") for f in multiselect]
    walking_data = WalkingData(recordings)
    return walking_data

def handle_plots_and_selectbox(walking_data : WalkingData) -> None:
    plot_names = walking_data.get_plot_names()
    with st.container():
        if walking_data.is_empty():
            st.write("### Veuillez sélectionner des fichiers à analyser")
        else:
            segmented_control = st.segmented_control(
                label="Type de graphe :",
                options=plot_names,
                selection_mode="single",
                default="Line"
            )
            if segmented_control:
                walking_data.cache_plots[segmented_control].show()

def main():
    st.set_page_config(page_title="R7 Visualisation", layout="wide")
    all_files = get_all_files()
    walking_data = handle_multiselect(all_files)
    walking_data.make_all_plots()
    handle_plots_and_selectbox(walking_data)
    

if __name__ == '__main__':
    main()
