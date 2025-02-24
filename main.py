"""
Module main de l'application Streamlit
Pour le lancer : streamlit run main.py
"""
import glob
import os
from typing import Dict
import streamlit as st
import pandas as pd
from src.walking_data import WalkingData
from src.walking_recording import WalkingRecording

def setup() ->  Dict:
    """
    Fonction de setup de l'application
    Permet de récupérer les données des membres du groupe

    Returns:
        Dict: Dictionnaire contenant les données des membres
    """
    file_path = 'data/processed'
    members_list = glob.glob(f"{file_path}/*")
    members_dict = {}
    
    for member in members_list:
        member_name = os.path.basename(member)
        members_dict[member_name] = {}
        file_list = glob.glob(f"{member}/*")
        for csv_file in file_list:
            members_dict[member_name][os.path.basename(csv_file)] = WalkingRecording.from_csv(csv_file)

    return members_dict

def main2():
    members = setup()
    members_names = list(members.keys())
    st.set_page_config(page_title="R7 Visualisation", layout="wide")
    walking_data = WalkingData([])
    st.title("Analyse des démarches des membres du groupe r7")
    with st.sidebar:
        recordings = []
        st.markdown("## Sélectionnez les fichiers à analyser")
        for name in members_names:
            file_names = (members[name].keys())
            select_box = st.selectbox(
                f"Choisissez un fichier pour {name}", 
                file_names,
                index=None
            )
            if select_box:
                recordings.append(members[name][select_box])
                st.write(f"Vous avez choisi {select_box}")
        walking_data = WalkingData(recordings)
        walking_data.make_all_plots()
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
    
def main() -> None:
    """
    Fonction principale de l'application
    """
    members = setup()
    members_names = list(members.keys())
    st.set_page_config(page_title="R7 Visualisation", layout="wide")
    st.title("Analyse des démarches des membres du groupe r7")
    with st.sidebar:
        dfs = []
        names = []
        st.markdown("## Sélectionnez les fichiers à analyser")
        for name in members_names:
            records = members[name]["records"]
            file_names = list(records.keys())
            select_box = st.selectbox(
                f"Choisissez un fichier pour {name}", 
                file_names,
                index=None
            )
            if select_box:
                st.write(f"Vous avez choisi {select_box}")
                dfs.append(members[name]["records"][select_box])
                names.append(name)
        movement_data = MovementData(dfs,names)
        plot_names = movement_data.get_plot_names()
        plots = movement_data.make_all_plots()

    with st.container():
        if not plot_names:
            st.write("### Veuillez sélectionner des fichiers à analyser")
        else:
            segmented_control = st.segmented_control(
                label="Type de graphe :",
                options=plot_names,
                selection_mode="single",
                default="Line"
            )
            if segmented_control:
                plots[segmented_control].show()

if __name__ == '__main__':
    main2()
