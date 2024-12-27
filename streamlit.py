import streamlit as st
import sqlite3
import pandas as pd
import duckdb

# Charger les datasets dans DuckDB (en mémoire)
@st.cache_resource
def load_database():
    conn = duckdb.connect(":memory:")  # Base DuckDB en mémoire
    datasets = {
        "users": pd.read_csv("users.csv"),
        "money": pd.read_csv("money.csv"),
        "cyberops": pd.read_csv("cyberops.csv"),
    }
    for name, df in datasets.items():
        conn.execute(f"CREATE TABLE {name} AS SELECT * FROM df")  # Crée chaque table dans DuckDB
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

# Initialisation du niveau débloqué
if 'unlocked_levels' not in st.session_state:
    st.session_state.unlocked_levels = {1: True}  # Niveau 1 débloqué par défaut

# Affichage des niveaux disponibles
available_levels = {1: "Niveau 1", 2: "Niveau 2", 3: "Niveau 3", 4: "Niveau 4", 5: "Niveau 5"}

# Vérifier quel niveau est débloqué
unlocked_levels = {level: available_levels[level] for level in st.session_state.unlocked_levels if st.session_state.unlocked_levels[level]}

# Choisir un niveau
choice = st.sidebar.radio("Choisissez un niveau", list(unlocked_levels.values()))

# Récupérer le niveau choisi
level = [k for k, v in available_levels.items() if v == choice][0]

# Afficher le niveau choisi
st.title(f"SQL Injection Challenge - {available_levels[level]}")

# Informations sur le niveau
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
                result = pd.read_sql_query(query, conn)
                if result.empty:
                    st.warning("Aucun résultat trouvé.")
                else:
                    st.success("Requête exécutée avec succès.")
                    st.write(result)
                    # Si la requête est réussie pour le niveau actuel, débloquer le niveau suivant
                    if level < 5 :
                        st.session_state.unlocked_levels[level + 1] = True
            except Exception as e:
                st.error(f"Erreur lors de l'exécution de la requête : {e}")

# Pour le niveau 5, afficher un indice sur les flags
if level == 5:
    st.write("Indice : Les morceaux du flag sont dans la table 'cyberops'.")
