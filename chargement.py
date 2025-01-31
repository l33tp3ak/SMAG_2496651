import os
import json
import datetime


# ------------------------- 1. DICTIONNAIRES DES PARAMÈTRE ENVIRONNEMENTAUX --------------------------


 # CHARGEMENT SAUVERGARDER DONNÉES
         


def open_data(fichier):
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:  # Vérifie si le fichier n'est pas vide
                file_data = json.loads(content)
                print("Donnée chargée avec succès")
                return file_data
            else:
                print(f"Le fichier {fichier} est vide. Initialisation avec les données par défaut.")
    # Crée le fichier avec les données par défaut si vide ou inexistant
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=2)
        f.close()
    print(f"Fichier {fichier} créé avec succès avec les données par défaut.")
    return {}



def write_data(fichier, data_dump):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data_dump, f, indent=2)
        f.close()
    return data_dump