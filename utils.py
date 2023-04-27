import spacy
import nltk
from nltk.util import ngrams

nltk.download('punkt')

# Charger le modèle de langue française de spaCy
nlp = spacy.load("fr_core_news_sm")

def preprocess_text(text, n=1, remove_stop_words=True, lemmatize=True, lowercase=True): # vous pouvez changer le n pour augmenter le nb de mots dans un token (1, 2, 3, ...)
                                                                                        # vous pouvez changer la valeur de remove_stop_words (False ou Truth)
                                                                                        # vous pouvez changer la valeur de lemmatize (False ou Truth)
                                                                                        # vous pouvez changer la valeur de lowercase (False ou Truth)
    # Suppression de la ponctuation spécifique
    punctuation = "«»—" # il reste des ponctuations qui peuvent être utiles ou non pour capter les styles : “”‘’()…?!.,;'-[]|{}
    for char in punctuation:
        text = text.replace(char, "")

    # Tokenisation
    tokens = [token.text for token in nlp(text)]

    # Mise en minuscule si lowercase est True
    if lowercase:
        tokens = [token.lower() for token in tokens]

    # Lemmatisation avec spaCy si lemmatize est True
    if lemmatize:
        spacy_text = nlp(" ".join(tokens))
        tokens = [token.lemma_ for token in spacy_text]

    # Suppression des mots vides
    if remove_stop_words:
        nltk.download('stopwords')
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('french'))
        tokens = [token for token in tokens if token.lower() not in stop_words]

    # N-grammes
    n_grams = list(ngrams(tokens, n))
    n_grams = [' '.join(grams) for grams in n_grams]

    # Jointure des mots pour créer le texte pré-traité
    preprocessed_text = ' '.join(n_grams)
    
    return preprocessed_text
