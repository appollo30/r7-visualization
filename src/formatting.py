import pandas as pd
import numpy as np
import glob

def trim(df):
    first_sec = df.iloc[0]["Timestamp"]
    last_sec = df.iloc[-1]["Timestamp"]

    df = df.query("Timestamp > @first_sec & Timestamp < @last_sec")

    return df

def set_time(df):
    df['time (s)'] = (df['Timestamp'] - df['Timestamp'].iloc[0]).dt.total_seconds()
    group = df.groupby("Timestamp")

    for idx, (name, group_df) in enumerate(group):
        group_df["time (s)"] = idx + np.linspace(0, 1, len(group_df)+1)[:-1]
        
        df.update(group_df)
    
    return df

if __name__ == "__main__":
    files = glob.glob("../data/input/**")
    print(files)