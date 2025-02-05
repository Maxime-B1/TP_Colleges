# importation des bibliothèques nécessaires
import requests
import os
import csv

def recupere_donnes():
    """
    Retourne les données sous forme d'une liste de dictionnaires
    """
    local_file = "college_finistere.csv" #nom donné au fichier
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
        
etablissements = recupere_donnes()

print(etablissements[0:10])