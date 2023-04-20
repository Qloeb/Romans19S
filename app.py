from flask import Flask, render_template, request
from utils import *

# Initialisation de l'application Flask
app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/', methods=['GET', 'POST'])
def home():

    dict_models = {
        'lr':LogisticRegression(solver='liblinear', multi_class='auto'),
        'mnb': MultinomialNB(),
        #'lsvc': LinearSVC(),
        'dt': DecisionTreeClassifier(max_depth=10),
        'rf': RandomForestClassifier(max_depth=10),
        'ada': AdaBoostClassifier(),
    }

    #Sera à remplacer par un appel du model avec les bon poids directement
    textes, labels = import_data("data")
    textes, labels = rassembler_textes_et_labels(textes, labels)

    if request.method == 'POST':

        print("Requête reçue")
        user_text = [request.form['text_input']]
        selected_model = request.form["selection"]
        selected_model = dict_models[selected_model]
        pipe = train_model(textes, labels, selected_model)
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