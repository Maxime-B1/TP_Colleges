# importation des bibliothèques nécessaires
import requests
import os
import csv
import pandas as pd
import folium

def recupere_donnes_finistere():
    """
    Retourne les données sous forme d'une liste de dictionnaires
    """
    local_file = "college_finistere.csv"

    if not os.path.exists(local_file):
        # recuperation des données depuis l'url
        url = "https://geobretagne.fr/geoserver/cd29/wfs?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=cd29%3Acolleges_29&OUTPUTFORMAT=csv"
        data = requests.get(url).content # on récupère les données sous forme de bytes
        # création d'un fichier et écriture des données
        with open(local_file, 'wb') as csvfile: # 'w' pour write et 'b' pour bytes
            csvfile.write(data)
    
    donnes = []
    # ouverture du fichier précédemment créé
    with open(local_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for ligne in reader:
            donnes.append(ligne)
    return donnes
        
etablissements = recupere_donnes_finistere()


def filtrer(donnes, criteres):
    result = []
    compteur = 0
    for ecole in donnes :
        for critere in criteres.keys() :
            if ecole[critere] == criteres[critere] :
                compteur += 1
        if compteur == len(criteres) :
            result.append(ecole['NOM_ET'])
        compteur = 0
    return result

#print(filtrer(etablissements, {'INSEE_COMM': '29232', 'STATUT' : 'Privé'}))

def trier(donnees, criteres):
    """
    donnees (liste) : une liste de colleges
    critères (liste) : la liste des colonnes à trier
    Retourne la liste triée des colleges.
    """
    def les_criteres(p):
        result = []
        for critere in criteres:
            result.append(p[critere])
        return result

    return sorted(donnees, key=les_criteres)

#print(trier(etablissements, ['STATUT', 'NOM_ET']))

def recupere_donnes_morbian():
    url = "https://www.data.gouv.fr/fr/datasets/r/bf9d46b1-5430-4866-ab7d-58a4d794324d"
    colleges_morbihan = pd.read_csv(url, delimiter=';', encoding='iso 8859-15')
    return colleges_morbihan

colleges_morbihan = recupere_donnes_morbian()



# le fichier est volumineux, à télécharger une seule fois
def recupere_donnes_france():
    local_file = "geolocalisation.csv"
    if not local_file in os.listdir():
        url = "https://data.education.gouv.fr/explore/dataset/fr-en-adresse-et-geolocalisation-etablissements-premier-et-second-degre/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B"
        data = requests.get(url).content
        with open(local_file, 'wb') as csvfile:
            csvfile.write(data)
    geolocalisations = pd.read_csv(local_file, delimiter = ";")
    return geolocalisations

colleges_france = recupere_donnes_france()
#print(geolocalisations)

mapper = {'CODE':'numero_uai',
         }

colleges_morbihan.rename(columns=mapper, inplace=True)
#print("La liste des établissements du morbihan")
#print(colleges_morbihan)

fusion = colleges_morbihan.merge(colleges_france, on=['numero_uai'], how='inner')
#print(fusion)


# à faire sur Colab

m = folium.Map([48.065431230705784,-2.9624202990714488], zoom_start=9)

for i in fusion.index:
    p = fusion["position"][i]
    latitude, longitude = p.split(",")

    folium.Marker(
        location=[float(latitude), float(longitude)],
        tooltip=fusion["PATRONYME"][i],
        popup=fusion["appellation_officielle"][i],
        icon=folium.Icon(color="green"),
    ).add_to(m)

m.save("Bureau/NSI/TP_Colleges/colleges_morbihan.html")

#fin