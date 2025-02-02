import os
import json
import csv
from datetime import datetime
# ------------------------- 1. LISTES DES PARAMÈTRES ENVIRONNEMENTAUX --------------------------

def open_env_data(fichier):
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:  # Vérifie si le fichier n'est pas vide
                file_data = json.loads(content)
                print("Données chargées avec succès")
                return file_data
            else:
                print(f"Le fichier {fichier} est vide. Initialisation avec une liste vide.")
    # Crée le fichier avec une liste vide si vide ou inexistant
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)  # Initialise avec une liste vide [] au lieu d'un dictionnaire {}
    print(f"Fichier {fichier} créé avec succès avec une liste vide.")
    return []  # Retourne une liste vide au lieu d'un dictionnaire vide

def write_data(fichier, data_dump):
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data_dump, f, indent=2)
    return data_dump




# ================= Partie 2 creation de tout les fichier json en cas ou il en aurrai pas, les fonction sont apeller dans main.py

    # 1  Vérifie si le fichier existe pour Alertes.py
def get_alerts(fichier):

    if not os.path.exists(fichier):
        # Crée le fichier avec une liste vide
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
        print(f"Le fichier {fichier} n'existait pas. Un fichier vide a été créé.")
        return 0
    
    # Si le fichier existe, lit et retourne le nombre d'alertes
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)
        return len(data)


    # 2  Structure par défaut pour environment.json utiliser seulement pour initialiser un fichier environement.json
def load_environment(fichier):
    default_data = [
        {
            "Date": "2024-12-01 08:00",
            "Température": 25.0,
            "Humidité": 60,
            "Lumière": 300,
            "CO2": 400
        },
        {
            "Date": "2024-12-01 12:00",
            "Température": 28.0,
            "Humidité": 55,
            "Lumière": 800,
            "CO2": 420
        }
    ]
    
    # Vérifie si le fichier existe
    if not os.path.exists(fichier):
        # Crée le fichier avec la structure par défaut
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        print(f"Le fichier {fichier} n'existait pas. Un fichier par défaut a été créé.")
    
    # Ouvre et lit le fichier JSON
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    return data


# ------------------------- 3. GESTION DES SEUILS OPTIMAUX --------------------------

def load_optimal_thresholds(fichier):
    """Charge ou crée le fichier de seuils optimaux avec des valeurs par défaut"""
    # Valeurs par défaut pour les paramètres
    default_data = {
        "Température": {"min": 20, "max": 30},
        "Humidité": {"min": 50, "max": 70},
        "Lumière": {"min": 200, "max": 1000},
        "CO2": {"min": 350, "max": 450}
    }

    # Création du fichier s'il n'existe pas
    if not os.path.exists(fichier):
        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        print(f"Fichier {fichier} créé avec les seuils par défaut.")
    
    # Lecture du fichier et vérification de base
    with open(fichier, "r", encoding="utf-8") as f:
        data = json.load(f)
        
        # Vérification minimale de la structure
        if not all(key in data for key in ["Température", "Humidité", "Lumière", "CO2"]):
            print("Structure de fichier invalide, réinitialisation avec les valeurs par défaut")
            with open(fichier, "w", encoding="utf-8") as f:
                json.dump(default_data, f, indent=4)
            return default_data
            
    return data



# ------------------------- 4. SAUVEGARDE CSV --------------------------
def save_to_csv(data, filename, mode='a'):
    """
    Sauvegarde les données dans un CSV avec gestion d'erreur améliorée
    Format des colonnes : Date;Température;Humidité;Lumière;CO2
    """
    if not data:
        raise ValueError("Aucune donnée fournie pour l'export CSV")
    
    # Vérification du format des données
    required_keys = ["Date", "Température", "Humidité", "Lumière", "CO2"]
    if not all(key in data[0] for key in required_keys):
        raise ValueError("Structure de données invalide pour l'export CSV")

    # Création du dossier d'export si nécessaire
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    try:
        with open(filename, mode, newline='', encoding='utf-8-sig') as f:
            # [...]
         print(f"Fichier créé avec succès : {os.path.abspath(filename)}")  # Debug
        return filename
    except Exception as e:
        print(f"ERREUR DÉTAILLÉE - {str(e)}")  # Log technique
        raise

def export_full_data_to_csv():
    """Exporte toutes les données environnementales dans un nouveau fichier CSV"""
    try:
        data = open_env_data("environment.json")
        if not data:
            raise ValueError("Aucune donnée à exporter")
            
        # Vérification de la structure
        required_keys = ["Date", "Température", "Humidité", "Lumière", "CO2"]
        if not all(key in data[0] for key in required_keys):
            raise ValueError("Structure de données invalide")
            
        # Création du dossier d'export
        export_dir = "exports_csv"
        os.makedirs(export_dir, exist_ok=True)
        
        # Génération du nom de fichier
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(export_dir, f"export_serre_{timestamp}.csv")
        
        # Écriture du fichier
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=required_keys, delimiter=';')
            writer.writeheader()
            writer.writerows(data)
            
        return filename
        
    except Exception as e:
        print(f"[ERREUR CSV] {str(e)}")
        raise