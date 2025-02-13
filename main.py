import streamlit as st
import pandas as pd
import glob
import os

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
    graph_to_display = None
    
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
    

if __name__ == '__main__':
    main()