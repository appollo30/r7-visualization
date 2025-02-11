import pandas as pd
import numpy as np
import glob
import os

def trim(df):
    first_sec = df.iloc[0]["Timestamp"]
    last_sec = df.iloc[-1]["Timestamp"]

    df = df.query("Timestamp > @first_sec & Timestamp < @last_sec")

    return df

def set_time(df):
    df['time (s)'] = 0
    group = df.groupby("Timestamp")

    for idx, (name, group_df) in enumerate(group):
        group_df["time (s)"] = idx + np.linspace(0, 1, len(group_df)+1)[:-1]
        
        df.update(group_df)
    
    return df

if __name__ == "__main__":
    input_path = glob.glob("../data/input/*")
    # Les noms de chaque membre du groupe, associés aux chemins de leurs fichiers
    members_names = {os.path.basename(elt) : elt for elt in input_path}
    
    for name, path in members_names.items():
        input_files = glob.glob(f"{path}/*")
        print(name)
        for f in input_files:
            df = pd.read_csv(f)
            df = trim(df)
            df = set_time(df)
            output_dir = f"../data/output/{name}"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            df.to_csv(f"{output_dir}/{os.path.basename(f)}", index=False)