from bs4 import BeautifulSoup
import pandas as pd
import requests

#Nom du csv
name        = "hockey.csv"

#On initialise les variables pour chaque colonne
content     = []
result      = {}
csv         = {}

for i in range(10):
    url         = "https://www.scrapethissite.com/pages/forms/?page_num=" + str(i+1)
    session     = requests.Session()
    reponse     = session.get(url)
    soup        = BeautifulSoup(reponse.text, "html.parser")

    #On crée le header
    for header in soup.find_all("th"):
        result[header.getText().strip()] = ""
    
    #On bloucle sur les équipes
    for team in soup.find_all("tr", {"class": "team"}):
        #On récupère les lignes avec les valeurs suivantes
        if int(team.find("td", {"class": "ga"}).getText().strip()) < 300 and int(team.find("td", {"class": "diff"}).getText().strip()) > 0:
            # On bloucle sur toutes les infos de l'équipe
            for index, info in enumerate(team.find_all("td")):
                content.append([])
                content[index].append(info.getText().strip())

    #Création de l'objet result avec les différents tableaux 
    for index, value in enumerate(result.items()):
        csv[value] = content[index]

#Création du Data frame avec les valeurs finales (On supprime les lignes vides)
rt = pd.DataFrame(csv).dropna()

#Ajout de la colonne 'id' auto incrémentée
# rt.insert(0, "id", range(1, len(rt) + 1))

#On crée le csv
rt.dropna().to_csv(name, index=False)