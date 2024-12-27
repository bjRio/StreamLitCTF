import streamlit as st

# Titre de la page
"""st.title("🎉 You Found the Flag Page! 🎉")

# Message principal
st.header("Flag Found? 🤔")
st.write("You think you’ve done it, huh? Let me give you a little something...")

# Faux flag
fake_flag = "FLAG{N1c3_Try_Keep_L00k1ng}"
st.code(fake_flag, language="text")

# Message amusant
st.write("---")
st.write("But wait... since you made it all the way here, I might as well share a secret with you.")

# Secret pour l'admin
st.write("**I only share my real secret with the admin. Go ahead, try again!** 😉")

# Message incitant à chercher le répertoire GitHub
st.write("🕵️‍♂️ Want a special gift? Head to my [GitHub and check for a surprise gift! 🎁")

# Petit style pour l'esthétique
st.markdown(
    """"""
    <style>
    body {
        background-color: #1e1e1e;
        color: #00ff00;
        font-family: "Courier New", Courier, monospace;
    }
    </style>
    ""","""
    unsafe_allow_html=True
)

# Lien retour
if st.button("Return to the main app"):
    st.write("Redirecting you... 🚀")"""

import streamlit as st
import duckdb
import pandas as pd
import re

# Charger les datasets
path = "/mnt/data/"  # Remplace par ton chemin local si nécessaire
datasets = {
    "users": pd.read_csv(f"{path}users.csv"),
    "money": pd.read_csv(f"{path}money.csv"),
    "cyberops": pd.read_csv(f"{path}cyberops.csv"),
}

# Fonction pour valider les requêtes selon le niveau
def validate_query(level, query):
    filters = {
        1: [],  # Pas de filtres
        2: [r'--', r';', r"'"],  # Bloque les commentaires et les guillemets simples
        3: [r'SELECT', r'FROM', r'DROP'],  # Bloque les mots-clés basiques
        4: [r'0x', r'FROM_BASE64'],  # Bloque les obfuscations hexadécimales et base64
        5: [r'.*'],  # Protection maximale
    }
    for pattern in filters[level]:
        if re.search(pattern, query, re.IGNORECASE):
            return False
    return True

# Fonction pour exécuter les requêtes
def execute_query(query, dataset_name):
    try:
        dataset = datasets[dataset_name]
        query_result = duckdb.query(query).to_df()
        return query_result
    except Exception as e:
        return f"Erreur dans la requête : {e}"

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
            # Détecter le dataset ciblé dans la requête
            if "users" in query.lower():
                dataset_name = "users"
            elif "money" in query.lower():
                dataset_name = "money"
            elif "cyberops" in query.lower():
                dataset_name = "cyberops"
            else:
                st.error("Aucun dataset valide trouvé dans la requête.")
                dataset_name = None

            if dataset_name:
                # Exécuter la requête et afficher les résultats
                result = execute_query(query, dataset_name)
                if isinstance(result, str):
                    st.error(result)
                else:
                    if result.empty:
                        st.warning("Aucun résultat trouvé.")
                    else:
                        st.success("Requête exécutée avec succès.")
                        st.write(result)

# Pour le niveau 5, afficher un indice sur les flags
if level == 5:
    st.write("Indice : Les morceaux du flag sont dans la table 'cyberops'.")

