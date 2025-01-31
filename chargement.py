import os
import json
import csv


# ------------------------- 1. DICTIONNAIRES DES PARAMÈTRES ENVIRONNEMENTAUX --------------------------

# Environnement data dump
env_data_dump = {
    "2024-12-01 12:00": {"Température": 22.5, "Humidité": 50.0, "Lumière": 300.0, "CO2": 400.0},
    "2024-12-01 12:02": {"Température": 23.0, "Humidité": 52.0, "Lumière": 310.0, "CO2": 410.0},
    "2024-12-01 12:04": {"Température": 22.8, "Humidité": "", "Lumière": 305.0, "CO2": ""}
}

# Seuil data dump
seuil_data_dump = {
    "2024-12-01 12:00": {"Température": 25.0, "Humidité": 60.0, "Lumière": 500.0, "CO2": 1000.0},
    "2024-12-01 12:02": {"Température": 26.0, "Humidité": 65.0, "Lumière": 550.0, "CO2": 1200.0},
    "2024-12-01 12:04": {"Température": 24.5, "Humidité": "", "Lumière": "", "CO2": 1100.0}
}

# Alertes data dump
alertes_data_dump = {
    "2024-12-01 12:00": {"Paramètre": "Température", "Valeur": 26.0, "Message": "Alerte: Température élevée"},
    "2024-12-01 12:02": {"Paramètre": "Humidité", "Valeur": 70.0, "Message": "Alerte: Humidité élevée"},
    "2024-12-01 12:04": {"Paramètre": "CO2", "Valeur": 1500.0, "Message": "Alerte: CO2 élevé"}
}


# ------------------------- 2. FONCTION POUR CHARGER LES DONNÉES --------------------------

def open_env_data(fichier, data_dump):
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
        json.dump(data_dump, f, ensure_ascii=False)
    print(f"Fichier {fichier} créé avec succès avec les données par défaut.")
    return data_dump


# Charger les données
environment_data = open_env_data("environment.json", env_data_dump)
seuil_data = open_env_data("seuil.json", seuil_data_dump)
alertes_data = open_env_data("alertes.json", alertes_data_dump)


# ------------------------- 3. FONCTION POUR SAUVEGARDER EN CSV --------------------------

def save_to_custom_csv(filename, data):
    """
    Save data to a custom CSV file in key-value pair format.
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for date, values in data.items():
            # Write the date
            writer.writerow([f"Date: {date}"])
            # Write each key-value pair
            for key, value in values.items():
                writer.writerow([f"{key}: {value}"])
            # Add an empty row for separation (optional)
            writer.writerow([])
    print(f"Données sauvegardées avec succès dans le fichier CSV {filename}.")


# Sauvegarder les données environnementales
save_to_custom_csv("environment_data.csv", environment_data)

# Sauvegarder les seuils
save_to_custom_csv("seuil_data.csv", seuil_data)

# Sauvegarder les alertes
save_to_custom_csv("alerts.csv", alertes_data)

print("Données sauvegardées avec succès dans les fichiers CSV.")