from flask import Flask, render_template, request
from utils import *

# Initialisation de l'application Flask
app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/', methods=['GET', 'POST'])
def home():

    #Sera à remplacer par un appel du model avec les bon poids directement
    textes, labels = import_data("data")
    textes, labels = rassembler_textes_et_labels(textes, labels)
    pipe = train_model(textes, labels)

    if request.method == 'POST':
        user_text = [request.form['user_input']]
        # Vous pouvez maintenant utiliser 'user_text' dans votre programme
        pred = pipe.predict(user_text)
        proba = pipe.predict_proba(user_text)
        print("Prédiction:", pred)
        print("Proba:", proba)
        return render_template('index.html', message="Texte envoyé avec succès!",
                               prediction=pred, probabilities=proba[0].tolist())
    return render_template('index.html', message="Entrez votre texte et cliquez sur Envoyer.")

# Exécution de l'application
if __name__ == '__main__':
    app.run(debug=True)