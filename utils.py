from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from bs4 import BeautifulSoup
import os

def import_data(path):

    textes = []
    labels = []

    for file in os.listdir(path):

        path_file = os.path.join(path, file)

        if os.path.isfile(path_file):

            with open(path_file) as fp:
                soup = BeautifulSoup(fp, "html.parser")

            paragraphes = soup.select("p")
            for p in paragraphes:
                texte = p.get_text()
                textes.append(texte)
                labels.append(file.split("-")[0])

    print("Nombre d'échantillons importés")
    print("Balzac :",labels.count("balzac"))
    print("Flaubert :",labels.count("flaubert"))
    print("Maupassant :",labels.count("maupassant"))
    print("Sand :",labels.count("sand"))
    print("Zola :",labels.count("zola"))

    return textes, labels

def rassembler_textes_et_labels(textes, labels, taille_minimale=1000):
    textes_rassembles = []
    labels_rassembles = []

    buffer_texte = ""
    buffer_label = ""

    for texte, label in zip(textes, labels):
        if buffer_label == "":
            buffer_label = label

        if buffer_label == label:
            buffer_texte += " " + texte
            if len(buffer_texte) >= taille_minimale:
                textes_rassembles.append(buffer_texte)
                labels_rassembles.append(buffer_label)
                buffer_texte = ""
                buffer_label = ""
        else:
            if len(buffer_texte) >= taille_minimale:
                textes_rassembles.append(buffer_texte)
                labels_rassembles.append(buffer_label)
            buffer_texte = texte
            buffer_label = label

    # Ajoute le dernier échantillon s'il n'a pas été ajouté précédemment et s'il est assez long
    if buffer_label and len(buffer_texte) >= taille_minimale:
        textes_rassembles.append(buffer_texte)
        labels_rassembles.append(buffer_label)

    print("Nombre d'échantillons rassemblés")
    print("Balzac :",labels_rassembles.count("balzac"))
    print("Flaubert :",labels_rassembles.count("flaubert"))
    print("Maupassant :",labels_rassembles.count("maupassant"))
    print("Sand :",labels_rassembles.count("sand"))
    print("Zola :",labels_rassembles.count("zola"))

    return textes_rassembles, labels_rassembles


def train_model(textes, labels):
    # Création d'un pipeline pour la transformation des données et l'entraînement du modèle
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),  # Transformation des textes en vecteurs TF-IDF
        ('classifier', LogisticRegression(solver='liblinear'))  # Classification avec la régression logistique
    ])

    # Entraînement du modèle
    pipeline.fit(textes, labels)

    return pipeline
