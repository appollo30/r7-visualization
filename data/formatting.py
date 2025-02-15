import os
import glob
import pandas as pd
import numpy as np

class DataFormatting:
    """
    Classe pour formater les données d'accélération
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def norm(self):
        """
        Calculer la norme du vecteur d'accélération

        Returns:
            pd.DataFrame: Le dataframe avec la norme du vecteur d'accélération comme nouvelle colonne
        """
        # Calculer la norme du vecteur d'accélération a = sqrt(x^2 + y^2 + z^2)
        self.df["acceleration (g)"] = np.sqrt(self.df["X (g)"]**2 + self.df["Y (g)"]**2 + self.df["Z (g)"]**2)
    
    def trim(self):
        """
        Réduire les données pour supprimer la première et la dernière seconde de l'enregistrement

        Returns:
            pd.DataFrame: Le dataframe réduit
        """
        first_sec = self.df.iloc[0]["Timestamp"]
        last_sec = self.df.iloc[-1]["Timestamp"]

        # Garder uniquement les données entre la première et la dernière seconde exclues
        self.df = self.df.query("Timestamp > @first_sec & Timestamp < @last_sec")
    
    def set_time(self):
        """
        Définir la colonne de temps pour qu'elle soit comptée en secondes depuis le début de l'enregistrement

        Returns:
            pd.DataFrame: Le dataframe avec la colonne de temps définie
        """
        self.df = self.df.copy()
        self.df['time (s)'] = 0
        self.df['time (s)'] = self.df['time (s)'].astype(float)
        group = self.df.groupby("Timestamp")

        for idx, (name, group_df) in enumerate(group):
            group_df["time (s)"] = idx + np.linspace(0, 1, len(group_df)+1)[:-1]

            self.df.update(group_df)

        self.df["time (s)"] = self.df["time (s)"].astype(float)
    
    def process(self):
        """
        Appliquer les transformations sur le dataframe

        Returns:
            pd.DataFrame: Le dataframe transformé
        """
        self.df["Timestamp"] = pd.to_datetime(self.df["Timestamp"])
        self.norm()
        self.trim()
        self.set_time()
        self.df = self.df.drop(columns=["Timestamp"])
        self.df = self.df.set_index("time (s)")

if __name__ == "__main__":
    input_path = glob.glob("./input/*")
    # Les noms de chaque membre du groupe, associés aux chemins de leurs fichiers
    members_names = {os.path.basename(elt): elt for elt in input_path}

    for name, path in members_names.items():
        input_files = glob.glob(f"{path}/*")
        print(name)
        for f in input_files:
            df = pd.read_csv(f)
            print(f"Traitement de {f}")
            data = DataFormatting(df)
            data.process()
            df = data.df
            OUTPUT_DIR = f"./output/{name}"
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
            df.to_csv(f"{OUTPUT_DIR}/{os.path.basename(f)}", index=True)
