import streamlit as st

# Titre de la page
st.title("🎉 You Found the Flag Page! 🎉")

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
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: #00ff00;
        font-family: "Courier New", Courier, monospace;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Lien retour
if st.button("Return to the main app"):
    st.write("Redirecting you... 🚀")
