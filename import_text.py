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