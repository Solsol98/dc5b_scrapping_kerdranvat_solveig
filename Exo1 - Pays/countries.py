from bs4 import BeautifulSoup
import pandas as pd
import requests

#Nom du csv
name        = "countries.csv"

url         = "https://www.scrapethissite.com/pages/simple/"
session     = requests.Session()
reponse     = session.get(url)
soup        = BeautifulSoup(reponse.text, "html.parser")

#On initialise les variables pour chaque colonne
Country     = []	
Capital     = []	
Population  = []
Area        = []

#On bloucle sur les pays
for row in soup.find_all("div", {"class": "country"}):
    Country.append(row.find("h3", {"class": "country-name"}).getText().strip())
    Capital.append(row.find("span", {"class": "country-capital"}).getText().strip())
    Population.append(row.find("span", {"class": "country-population"}).getText().strip())
    Area.append(row.find("span", {"class": "country-area"}).getText().strip())

#Création de l'objet result avec les différents tableaux 
result = {
    "Country"       : Country,
    "Capital"       : Capital,
    "Population"    : Population,
    "Area (km2)"    : Area
}

#Création du Data frame avec les valeurs finales (On supprime les lignes vides)
rt = pd.DataFrame(result).dropna()

#Ajout de la colonne 'id' auto incrémentée
# rt.insert(0, "id", range(1, len(rt) + 1))

#On crée le csv
rt.dropna().to_csv(name, index=False)