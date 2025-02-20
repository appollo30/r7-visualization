"""
Module main de l'application Streamlit
Pour le lancer : streamlit run main.py
"""
import glob
import os
from typing import Dict
import streamlit as st
import pandas as pd
from src.movement_data import MovementData

def setup() ->  Dict:
    """
    Fonction de setup de l'application
    Permet de récupérer les données des membres du groupe

    Returns:
        Dict: Dictionnaire contenant les données des membres
    """
    file_path = 'data/processed'
    files = glob.glob(f"{file_path}/*")
    members = {os.path.basename(f) : {"path": f} for f in files}

    for member in members:
        members[member]["records"] = {}
        for record in glob.glob(f"{members[member]['path']}/*"):
            members[member]["records"][os.path.basename(record)] = pd.read_csv(record)

    return members


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
    main()
