from flask import Flask, render_template, request
from utils import *
from bokeh.embed import components
from bokeh.plotting import figure


# Initialisation de l'application Flask
app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# Route pour la page des prédictions (ancienne page d'accueil)
@app.route('/predictions', methods=['GET', 'POST'])
def predictions():

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

        # Graphique Bokeh
        labels = ['Balzac', 'Flaubert', 'Maupassant', 'Sand', 'Zola']
        probabilities = proba[0].tolist()
        p = figure(x_range=labels, plot_height=300, plot_width=500, title="Probabilités par auteur")
        p.vbar(x=labels, top=probabilities, width=0.9)

        # Passer les composants du graphique au modèle de rendu
        script, div = components(p)
        return render_template('predictions.html', message="Texte envoyé avec succès!",
                               prediction=pred, probabilities=proba[0].tolist(),
                               script=script, div=div)
    return render_template('predictions.html', message="Entrez votre texte et cliquez sur Envoyer.")


@app.route('/modeles', methods=['GET', 'POST'])
def modeles():
    return render_template('modeles.html')

# Exécution de l'application
if __name__ == '__main__':
    app.run(debug=True)