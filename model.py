from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from bs4 import BeautifulSoup
import os

path = "data"
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

print("Nombre d'échantillons")
print("Balzac :",labels.count("balzac"))
print("Flaubert :",labels.count("flaubert"))
print("Maupassant :",labels.count("maupassant"))
print("Sand :",labels.count("sand"))
print("Zola :",labels.count("zola"))

#######################################################################

# Création d'un pipeline pour la transformation des données et l'entraînement du modèle
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),  # Transformation des textes en vecteurs TF-IDF
    ('classifier', LogisticRegression(solver='liblinear'))  # Classification avec la régression logistique
])

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(textes, labels, test_size=0.2, random_state=42)

# Entraînement du modèle
pipeline.fit(X_train, y_train)

# Prédiction et évaluation du modèle
y_pred = pipeline.predict(X_test)

with open('output.txt', 'w') as f:
    print("Rapport de classification:\n", classification_report(y_test, y_pred), file=f)
    print("Matrice de confusion:\n", confusion_matrix(y_test, y_pred), file=f)

