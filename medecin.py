from bs4 import BeautifulSoup
import pandas as pd
import requests

#Nom du csv
name    = "medecin.csv"

#Variables
data    = []
i       = 0
session = requests.Session()
cookies = {
            'AmeliDirectPersist': '1265688887.42527.0000',
            'TS01b76c1f': '0139dce0d213d9ed850ac4ecb736f7308428992f22c2258050e862c3239ec14c1a89745f8197aac8204963a668eb84b0a0fb8cf29f',
            'infosoins': 'ovj631vfm3tum2d3uurrrqeak3',
        }
headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://annuairesante.ameli.fr/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

#On boucle pour parcourir les pages
for i in range(50):
    url      = "http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-" + str(i+1) + "-par_page-20-tri-distance_asc.html"
    reponse  = session.get(url, headers = headers, cookies = cookies)
    soup     = BeautifulSoup(reponse.text, "html.parser")

    #On boucle sur les medecins
    for medecin in soup.find_all('div', {'class': 'item-professionnel'}):
        #Nom du medecin
        name_medecin =  medecin.find('div', {'class': 'nom_pictos'})
        if name_medecin:
            data_name_medecin = name_medecin.getText()
        else:
            data_name_medecin = "Nom inconnu"

        #Telephone du medecin
        tel_medecin = medecin.find('div', {'class': 'tel'})
        if tel_medecin:
            data_tel_medecin = tel_medecin.getText()
        else:
            data_tel_medecin = "Telephone inconnu"

        #Adresse du medecin
        adresse_medecin = medecin.find('div', {'class': 'adresse'})
        if adresse_medecin:
            data_adresse_medecin = adresse_medecin.getText()
        else:
            data_adresse_medecin = "Adresse inconnu"

        #Ajouter les données au tableau
        data.append([data_name_medecin, data_tel_medecin, data_adresse_medecin])

#Création du Data frame avec les valeurs finales (On supprime les lignes vides)
rt = pd.DataFrame(data, columns=['Nom du medecin', 'Telephone', 'Adresse'])

#On crée le csv
rt.dropna().to_csv(name, index=False)