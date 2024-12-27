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

# Fonction pour chaque niveau
def verifier_payload(payload, niveau):
    """
    Vérifie si un payload est valide pour un niveau donné.
    """
    # Règles spécifiques par niveau
    filtres = {
        1: [],  # Aucun filtre
        2: ["'", "--", ";"],  # Filtrage basique
        3: ["union", "select", "' OR", "--"],  # Plus restrictif
        4: ["sleep", "benchmark", "' AND", "1=1"],  # Approfondi
        5: ["{", "}", "$", ":", "['", '["'],  # Protection NoSQL
    }

    # Vérifier si le payload est invalide (pas un vrai payload ou contient des mots-clés interdits)
    if not payload or any(keyword in payload.lower() for keyword in filtres[niveau]):
        return False, "Injection bloquée ou entrée invalide."

    # Si aucun mot interdit et qu'on simule une requête réussie
    return True, "Injection réussie!"

# Interface principale
st.title("CTF SQLi & NoSQLi")
st.write("Essayez de contourner les protections à chaque niveau.")

# Formulaires pour chaque niveau
for niveau in range(1, 6):
    st.header(f"Niveau {niveau}")
    payload = st.text_input(f"Payload pour le niveau {niveau}", key=f"niveau{niveau}")
    
    if st.button(f"Tenter l'injection - Niveau {niveau}", key=f"btn{niveau}"):
        success, message = verifier_payload(payload, niveau)
        if success:
            st.success(message)
        else:
            st.error(message)

