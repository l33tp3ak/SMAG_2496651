import os
import json
import csv
from datetime import datetime
# ------------------------- 1. LISTES DES PARAMÈTRES ENVIRONNEMENTAUX --------------------------

def open_data(fichier):
	# ------------------------- 1. DICTIONNAIRES PAR DEFAUT --------------------------
	# Crée la structure des dictionnaires par défaut dépendemment du fichier utilisé.
	if (fichier == "optimal_threshold.json"):
		defaut_values = {
			"Température": {"min": 20, "max": 30},
			"Humidité": {"min": 50, "max": 70},
			"Lumière": {"min": 200, "max": 1000},
			"CO2": {"min": 350, "max": 450}
		}
	else:
		defaut_values = {}


	# Si le fichier existe, on charge les donnees
	if os.path.exists(fichier):
		with open(fichier, "r", encoding="utf-8") as content:
			if content:  # Vérifie si le fichier n'est pas vide
				file_data = json.loads(content.read().strip())
				# Verifie si le fichier JSON contient la bonne structure et les cles necessaire. Sinon, les valeurs par defaut sont ajoutees
				if (fichier == "optimal_threshold.json" and (file_data.get("Température") == None or file_data.get("Humidité") == None or file_data.get("Lumière") == None or file_data.get("CO2") == None)):
					for cle, valeur in defaut_values.items():
						if (file_data.get(cle) == None):
							file_data.update({cle: valeur})
					# Ferme le fichier et exporte les données vers le fichier JSON
					content.close()
					write_data(fichier, file_data)
				print("Donn\u00E9e charg\u00E9e avec succ\u00E8s")
				return file_data
			else:
				print(f"Le fichier {fichier} n'existe pas. Initialisation avec les donn\u00E9es par d\u00E9faut.")
	# Crée le fichier avec les données par défaut si vide ou inexistant
	with open(fichier, "w", encoding="utf-8") as f:
		# Crée le fichier en utilisant les valeurs par défaut approprié
		json.dump(defaut_values, f, indent=2)
	print(f"Fichier {fichier} cr\u00E9\u00E9 avec succ\u00E8s avec les donn\u00E9es par d\u00E9faut.")
	return defaut_values

def write_data(fichier, data_dump):
	with open(fichier, "w", encoding="utf-8") as f:
		json.dump(data_dump, f, indent=2)
		f.close()
	return data_dump



# ------------------------- 4. SAUVEGARDE CSV --------------------------




def export_data_to_csv(data = open_data("environment.json"), file = None):
	"""Exporte toutes les données environnementales dans un nouveau fichier CSV"""
	print(data)
	if not data:
		raise ValueError("Aucune donnée à exporter")

	# Création du dossier d'export
	export_dir = "exports_csv"
	os.makedirs(export_dir, exist_ok=True)

	# Génération du nom de fichier
	if (file == None):
		file = f"export_serre_{datetime.now().strftime("%d %B %Y %I%M%S%p")}.csv"


	filename = os.path.join(export_dir, file)

	# Écriture du fichier
	with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
		if (file == "alertes.csv"):
			for date_fields in data:
				dates = []
				dates.append(date_fields)
				writer = csv.DictWriter(f, fieldnames=dates, delimiter=';')
				writer.writeheader()
				for parameter_fields in data[date_fields]:
					fields_pour_parametre = []
					fields_pour_parametre.append(parameter_fields)
					writer = csv.DictWriter(f, fieldnames=fields_pour_parametre, delimiter=';')
					writer.writeheader()
					fields = []
					for parameter in data[date_fields][parameter_fields]:
						fields.append(parameter)
					writer = csv.DictWriter(f, fieldnames=fields, delimiter=';')
					writer.writeheader()
					writer.writerow(data[date_fields][parameter_fields])
		else:
			for date_fields in data:
				dates = []
				dates.append(date_fields)
				writer = csv.DictWriter(f, fieldnames=dates, delimiter=';')
				writer.writeheader()
				fields = []
				for parameter in data[date_fields]:
					fields.append(parameter)
				writer = csv.DictWriter(f, fieldnames=fields, delimiter=';')
				writer.writeheader()
				writer.writerow(data[date_fields])

	return filename