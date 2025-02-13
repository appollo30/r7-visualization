import streamlit as st
import pandas as pd
import glob
import os
from src.plots import MovementData

def setup():
    file_path = 'data/output'
    files = glob.glob(f"{file_path}/*")
    members = {os.path.basename(f) : {"path": f} for f in files}
    
    for name, member in members.items():
        member["records"] = {}
        for record in glob.glob(f"{member['path']}/*"):
            member["records"][os.path.basename(record)] = pd.read_csv(record)
    
    return members
       

def main():
    members = setup()
    members_names = list(members.keys())
    
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
        plot_dict = movement_data.make_all_plots()
    
    with st.container():
        if not plot_dict:
            st.write("### Veuillez sélectionner des fichiers à analyser")
        else:
            segmented_control = st.segmented_control(
                label="Type de graphe :",
                options=list(plot_dict.keys()),
                selection_mode="single",
                default="Line"
            )
            st.plotly_chart(plot_dict[segmented_control])

if __name__ == '__main__':
    main()