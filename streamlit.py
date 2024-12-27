import os
import sqlite3
import pandas as pd

# Fonction pour charger et insérer les données CSV dans une base SQLite
def load_database():
    conn = sqlite3.connect(":memory:")  # Base SQLite en mémoire
    datasets = {
        "users": "users.csv",
        "money": "money.csv",
        "cyberops": "cyberops.csv",
    }

    for name, file_path in datasets.items():
        try:
            # Vérifier si le fichier existe
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Fichier {file_path} introuvable.")

            # Charger le fichier CSV et l'insérer comme table
            df = pd.read_csv(file_path)
            df.to_sql(name, conn, index=False, if_exists="replace")
            print(f"Table {name} créée avec succès.")
        except FileNotFoundError as e:
            print(f"Erreur : {e}")
        except Exception as e:
            print(f"Une erreur est survenue avec {file_path}: {e}")
    
    return conn

# Charger la base de données
conn = load_database()

# Exemple de requête pour vérifier que les tables ont bien été créées
try:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables disponibles :", tables)
except Exception as e:
    print(f"Erreur lors de la récupération des tables : {e}")
