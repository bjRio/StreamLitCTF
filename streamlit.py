import streamlit as st
import sqlite3
import pandas as pd
import duckdb
import re

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
    st.subheader("Niveau 1 : Page d'authentification")

    # Formulaire d'authentification
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username and password:
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            if not validate_query(level, query):
                st.error("Requête bloquée par les filtres de ce niveau.")
            else:
                try:
                    # Exécute la requête SQL sur la base
                    result = pd.read_sql_query(query, conn)
                    if result.empty:
                        st.error("Identifiants incorrects.")
                    else:
                        st.success("Connexion réussie.")
                        st.write(result)  # Affiche les résultats
                        
                        # Vérifie si l'utilisateur connecté est l'admin
                        if "admin" in result["username"].values:
                            st.success("Vous avez débloqué le niveau 2 !")
                            st.session_state.unlocked_levels[2] = True
                            st.session_state["refresh"] = True  # Actualisation
                except Exception as e:
                    st.error(f"Erreur lors de l'exécution de la requête : {e}")
        else:
            st.error("Veuillez entrer un nom d'utilisateur et un mot de passe.")

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
                    if level < 5:
                        st.session_state.unlocked_levels[level + 1] = True
                        # Ajouter un bouton "virtuel" qui déclenche une actualisation de la page
                        st.session_state["refresh"] = True  # Marque le besoin de rafraîchissement
            except Exception as e:
                st.error(f"Erreur lors de l'exécution de la requête : {e}")

# Simuler l'actualisation de la page si un nouveau niveau est débloqué
if "refresh" in st.session_state and st.session_state["refresh"]:
    st.session_state["refresh"] = False
    st.experimental_rerun()  # Force l'actualisation de la page

# Pour le niveau 5, afficher un indice sur les flags
if level == 5:
    st.write("Indice : Les morceaux du flag sont dans la table 'cyberops'.")
