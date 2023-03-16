from bs4 import BeautifulSoup

with open("maupassant-fort.htm") as fp:
    soup = BeautifulSoup(fp, "html.parser")

paragraphes = soup.select("p")
for p in paragraphes:
    texte = p.get_text()
    print(texte)
    