from flask import Flask, render_template, request
from utils import *
from bokeh.embed import components
from bokeh.plotting import figure
import pickle


# Initialisation de l'application Flask
app = Flask(__name__)

# Route pour la page d'accueil
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/modeles', methods=['GET', 'POST'])
def modeles():
    return render_template('modeles.html')

@app.route('/donnees', methods=['GET', 'POST'])
def donnees():
    return render_template('donnees.html')

# Route pour la page des prédictions (ancienne page d'accueil)
@app.route('/predictions', methods=['GET', 'POST'])
def predictions():

    if request.method == 'POST':

        print("Requête reçue")
        user_text = [request.form['text_input']]
        selected_model = request.form["selection"]

        user_text = preprocess_text(user_text[0])
        print(user_text)
        pipe = pickle.load(open("model/"+selected_model+"_model.pkl",'rb'))
        pred = pipe.predict([user_text])
        proba = pipe.predict_proba([user_text])

        print("Prédiction:", pred)
        print("Proba:", proba)

        # Graphique Bokeh
        labels = ['Balzac', 'Flaubert', 'Maupassant', 'Sand', 'Zola']
        probabilities = proba[0].tolist()
        p = figure(x_range=labels, height=300, width=500, title="Probabilités par auteur")
        p.vbar(x=labels, top=probabilities, width=0.9)

        # Passer les composants du graphique au modèle de rendu
        script, div = components(p)
        return render_template('predictions.html', message="Texte envoyé avec succès!",
                               prediction=pred[0], probabilities=proba[0].tolist(),
                               script=script, div=div)
    return render_template('predictions.html', message="Entrez votre texte et cliquez sur Envoyer.")

# Exécution de l'application
if __name__ == '__main__':
    app.run(debug=True)