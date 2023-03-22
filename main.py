import streamlit as st
import psycopg2

# Connexion à la base de données
conn = psycopg2.connect(
    host="localhost",
    database="inscrip",
    user="postgres",
    password="admin"
)

# Création de la table utilisateur
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateur
             (id SERIAL PRIMARY KEY,
             nom TEXT NOT NULL,
             prenom TEXT NOT NULL,
             email TEXT NOT NULL,
             mot_de_passe TEXT NOT NULL);''')
conn.commit()

# Fonction d'inscription
def inscription():
    st.write("## Inscription")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    if st.button("S'inscrire"):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO utilisateur (nom, prenom, email, mot_de_passe) VALUES (%s, %s, %s, %s)", (nom, prenom, email, mot_de_passe))
        conn.commit()
        st.success("Inscription réussie !")

# Fonction de connexion
def connexion():
    st.write("## Connexion")
    email = st.text_input("Email")
    mot_de_passe = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM utilisateur WHERE email=%s AND mot_de_passe=%s", (email, mot_de_passe))
        result = cursor.fetchone()
        if result:
            st.success("Connexion réussie !")
        else:
            st.error("Email ou mot de passe incorrect")

# Page d'accueil
def accueil():
    st.write("# Bienvenue")
    st.write("Veuillez vous inscrire ou vous connecter pour accéder à votre compte.")
    menu = ["Accueil", "Inscription", "Connexion"]
    choix = st.sidebar.selectbox("Menu", menu)
    if choix == "Accueil":
        pass
    elif choix == "Inscription":
        inscription()
    elif choix == "Connexion":
        connexion()

# Affichage de la page d'accueil
accueil()

# Fermeture de la connexion à la base de données
conn.close()
