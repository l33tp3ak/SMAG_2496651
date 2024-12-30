import csv
from fake_database import get_environment_data

def save_to_csv(filename, data):
    """Sauvegarde des données dans un fichier CSV.
    :param filename: Nom du fichier CSV.
    :param data: Liste de dictionnaires contenant les données.
    """
    with open(filename, mode='w', newline='') as file:  # Ouvre (ou crée) un fichier en mode écriture ('w').
        writer = csv.writer(file)                       # Crée un objet "writer" pour écrire dans le fichier CSV.
        writer.writerow(data[0].keys())                 # Utilise les clés du premier dictionnaire pour écrire les en-têtes du CSV (colonnes).
        for row in data:                                # Parcourt chaque dictionnaire dans la liste data.
            writer.writerow(row.values())               # Écrit les valeurs du dictionnaire dans le CSV.

def load_from_csv(filename):
    """Charge des données depuis un fichier CSV.
    :param filename: Nom du fichier CSV.
    :return: Liste de dictionnaires contenant les données.
    """
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)               # Lit le fichier CSV et retourne chaque ligne comme un dictionnaire.
            return list(reader)                         # Retourne toutes les lignes sous forme de liste de dictionnaires.
    except FileNotFoundError:
        print(f"Erreur : Le fichier {filename} est introuvable.")
        return []  # Retourne une liste vide si le fichier n'existe pas.

# TEST
# Charger les données simulées depuis fake_database
data = get_environment_data()

# Garder uniquement les 5 dernières données
last_five_data = data[-5:]

# Sauvegarder dans un fichier CSV
save_to_csv("environment_data.csv", data)
loaded_data = load_from_csv("last_five_records.csv")

# Charger depuis un fichier CSV
loaded_data = load_from_csv("environment_data.csv")
print("Données chargées :", loaded_data)



