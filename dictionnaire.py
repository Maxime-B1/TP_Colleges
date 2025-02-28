# importation des bibliothèques nécessaires
import requests
import os
import csv

def recupere_donnes():
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
        
etablissements = recupere_donnes()


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

print(trier(etablissements, ['STATUT', 'NOM_ET']))