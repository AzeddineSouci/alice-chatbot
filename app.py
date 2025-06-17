import streamlit as st
import string
import re


def lire_fichier(nom_fichier):
    with open(nom_fichier, "r", encoding="utf-8") as f:
        return f.read()


def preprocess(texte):
    # Supprimer l'en-tête et le pied de page de Project Gutenberg
    debut = texte.find("CHAPTER I")
    fin = texte.find("End of the Project Gutenberg")
    if debut != -1 and fin != -1:
        texte = texte[debut:fin]

    # Convertir en minuscules
    texte = texte.lower()

    # Remplacer les sauts de ligne par des espaces
    texte = texte.replace("\n", " ").replace("\r", " ")

    # Découper en phrases avec une expression régulière
    phrases = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", texte)

    # Filtrer les phrases trop longues ou trop courtes
    phrases_filtrees = []
    for phrase in phrases:
        phrase = phrase.strip()
        if (
            len(phrase) > 10 and len(phrase) < 200
        ):  # Garder les phrases de taille raisonnable
            phrases_filtrees.append(phrase)

    return phrases_filtrees


def trouver_phrase_pertinente(question, phrases):
    # Prétraiter la question
    question = question.lower()
    question = question.translate(str.maketrans("", "", string.punctuation))

    meilleure_phrase = ""
    meilleur_score = 0

    # Liste des mots de la question
    mots_question = question.split()

    for phrase in phrases:
        # Compter combien de mots de la question sont dans la phrase
        score = 0
        for mot in mots_question:
            if mot in phrase:
                score += 1

        # Préférer les phrases avec plus de correspondances
        if score > meilleur_score:
            meilleur_score = score
            meilleure_phrase = phrase

    return (
        meilleure_phrase
        if meilleure_phrase
        else "I don't know how to answer this question."
    )


def chatbot(question, phrases):
    return trouver_phrase_pertinente(question, phrases)


def main():
    st.title("Alice Chatbot")
    st.write("Ask me a question about the book! (What does Alice eat?) ")

    texte = lire_fichier("alice.txt")
    phrases = preprocess(texte)

    question = st.text_input("Votre question :")

    if question:
        with st.spinner("Le Lapin Blanc cherche la réponse..."):
            reponse = chatbot(question, phrases)

        st.subheader("Réponse :")
        st.write(reponse)


if __name__ == "__main__":
    main()
