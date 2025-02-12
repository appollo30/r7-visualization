import streamlit as st
import glob
import os
from src.utils import select_random_file
from src.plots import multi_line_graph
import pandas as pd

if __name__ == '__main__':
    input_path = glob.glob("./data/output/*")
    # Les noms de chaque membre du groupe, associés aux chemins de leurs fichiers
    members_names = {os.path.basename(elt) : elt for elt in input_path}
    
    st.title("Visualisation des données")
    
    selection = st.pills("Choisissez des membres du groupe",
                         list(members_names.keys()),
                         selection_mode="multi")
    
    dfs = []
    
    for member in selection:
        member_path = members_names[member]
        files = glob.glob(f"{member_path}/*")
        selected_file = select_random_file(files)
        dfs.append(pd.read_csv(selected_file))
    
    st.plotly_chart(multi_line_graph(dfs,selection))