import os
import json


# ------------------------- 1. DICTIONNAIRES DES PARAMÈTRE ENVIRONNEMENTAUX --------------------------

 # CHARGEMENT SAUVERGARDER DONNÉES
def open_env_data(fichier):
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
        json.dump([], f, ensure_ascii=False, indent=4)
    print(f"Fichier {fichier} créé avec succès avec les données par défaut.")
    return []


environment_data = open_env_data("environment.json")
alerts_data = open_env_data("alerts.json")
seuil_data= open_env_data("seuil.json")
#===========================================================================================


def get_alerts(fichier):
    """
    Récupère le nombre d'alertes à partir d'un fichier JSON.
    Le fichier doit contenir une liste d'alertes.
    """
    
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):  # Vérifie que les données sont une liste
            return len(data)  # Retourne le nombre d'alertes
           
def save_env_data(fichier, data):
    """Sauvegarde les données dans le fichier spécifié."""
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Données sauvegardées dans {fichier}")