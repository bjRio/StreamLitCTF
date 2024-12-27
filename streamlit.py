import streamlit as st
import duckdb
import pandas as pd
import re

# Charger les datasets dans DuckDB (en mémoire)
@st.cache_resource
def load_database():
    conn = duckdb.connect(database=":memory:")  # Base DuckDB en mémoire
    datasets = {
        "users": "users.csv",
        "money": "money.csv",
        "cyberops": "cyberops.csv",
    }
    for name, file_path in datasets.items():
        conn.execute(f"""
        CREATE TABLE {name} AS 
        SELECT * FROM read_csv_auto('{file_path}');
        """)
    return conn

conn = load_database()

# Fonction pour valider les requêtes selon le niveau
def validate_query(level, query):
    filters = {
        1: [],  # Pas de filtres
        2: [r'--', r';', r"'"],  # Bloque les commentaires et les guillemets simples
        3: [r'DROP', r'INSERT', r'UPDATE'],  # Bloque les commandes destructrices
        4: [r'0x', r'FROM_BASE64'],  # Bloque les obfuscations hexadécimales et base64
        5: [r'.*'],  # Protection maximale
    }
    for pattern in filters[level]:
        if re.search(pattern, query, re.IGNORECASE):
            return False
    return True

# Créer une barre latérale pour naviguer entre les niveaux
st.sidebar.title("SQL Injection Challenge")
options = {
    "Niveau 1": 1,
    "Niveau 2": 2,
    "Niveau 3": 3,
    "Niveau 4": 4,
    "Niveau 5": 5
}
choice = st.sidebar.radio("Choisissez un niveau", list(options.keys()))

# Afficher le contenu en fonction du niveau choisi
level = options[choice]
st.title(f"SQL Injection Challenge - {choice}")

if level == 1:
    st.subheader("Niveau 1 : Pas de filtre")
elif level == 2:
    st.subheader("Niveau 2 : Filtres basiques")
elif level == 3:
    st.subheader("Niveau 3 : Filtres avancés")
elif level == 4:
    st.subheader("Niveau 4 : Obfuscation bloquée")
elif level == 5:
    st.subheader("Niveau 5 : Protection maximale")

# Formulaire pour exécuter une requête SQL
st.write("Entrez votre requête SQL ci-dessous pour interagir avec la base de données.")
query = st.text_area("Requête SQL", height=100)

if st.button("Soumettre la requête"):
    if not query:
        st.error("Veuillez entrer une requête SQL.")
    else:
        if not validate_query(level, query):
            st.error("Requête bloquée par les filtres de ce niveau.")
        else:
            try:
                # Exécuter la requête SQL sur la base DuckDB
                result = conn.execute(query).fetchdf()
                if result.empty:
                    st.warning("Aucun résultat trouvé.")
                else:
                    st.success("Requête exécutée avec succès.")
                    st.write(result)
            except Exception as e:
                st.error(f"Erreur lors de l'exécution de la requête : {e}")

# Pour le niveau 5, afficher un indice sur les flags
if level == 5:
    st.write("Indice : Les morceaux du flag sont dans la table 'cyberops'.")
