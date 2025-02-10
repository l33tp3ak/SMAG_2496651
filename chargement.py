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
	if (file == "alertes.csv"):
		header = []


	# Écriture du fichier
	with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
		if (file == "alertes.csv"):
			# Aplatie le titre des colonnes à partir de notre dictionnaire extrait du JSON
			header = ["Date", "Paramètre"]
			for date_fields in data:
				rest_of_fields = []
				for parameter_fields in data[date_fields]:
					for parameter in data[date_fields][parameter_fields]:
						rest_of_fields.append(parameter)

			# Écrit le titre des colonnes
			header = header + rest_of_fields
			writer = csv.DictWriter(f, fieldnames=header, delimiter=';')
			writer.writeheader()

			# Ouvre notre CSV de nouveau pour écrire les données
			writer = csv.writer(f, delimiter=';')

			# Aplatie nos données extraites de notre JSON pour correspondre à nos colonnes
			for date_fields in data:
				for parameter_fields in data[date_fields]:
					# Chaque donnée de notre JSON doit avoir les clés précédentes répétées.
					# Celles-ci doivent donc être ajoutées just avant le plus bas niveau, pour chaque donnée, à toutes les fois.

					fields = [date_fields, parameter_fields]

					for parameter in data[date_fields][parameter_fields]:
						# On ajoute nos données, finalisant l'aplatissement
						fields.append(data[date_fields][parameter_fields][parameter])

					# Écrit nos données aplaties
					writer.writerow(fields)

		else:
			# Aplatie le titre des colonnes à partir de notre dictionnaire extrait du JSON
			header = ["Date"]
			param = open_data("optimal_threshold.json")
			for parameter in param:
				header.append(parameter)

			# Écrit le titre des colonnes
			writer = csv.DictWriter(f, fieldnames=header, delimiter=';')
			writer.writeheader()

			# Ouvre notre CSV de nouveau pour écrire les données
			writer = csv.writer(f, delimiter=';')

			# Aplatie nos données extraites de notre JSON pour correspondre à nos colonnes
			for date_fields in data:
				fields = [date_fields]
				for parameter in data[date_fields]:
					fields.append(data[date_fields][parameter])

				# Écrit nos données aplaties
				writer.writerow(fields)

	return filename