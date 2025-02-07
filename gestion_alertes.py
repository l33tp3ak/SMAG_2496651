# gestion_alertes.py

import tkinter as tk
from tkinter import ttk
from chargement import open_data
from datetime import datetime

def creer_fenetre_alertes(alertes_param = None, alertes_date = None):
	# Création de la fenêtre avec taille et couleur de fond
	fenetre = tk.Toplevel()
	fenetre.title("Liste des Alertes")
	fenetre.geometry("400x600")
	fenetre.configure(bg="#303030")  # Fond gris anthracite

	# Configuration du système de défilement (canvas + scrollbar)
	canvas = tk.Canvas(fenetre, bg="#303030", highlightthickness=0)
	scrollbar = ttk.Scrollbar(fenetre, orient="vertical", command=canvas.yview)
	scrollable_frame = ttk.Frame(canvas)  # Conteneur pour les alertes

	canvas.pack(side="left", fill="both", expand=True)
	scrollbar.pack(side="right", fill="y")
	canvas.configure(yscrollcommand=scrollbar.set)
	canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

	# Chargement des données depuis le fichier JSON
	alertes = open_data("alertes.json")
	groupes = {}
	if (alertes_param is None) and (alertes_date is None):
		for alerte in alertes:
			#print(alerte)
			#print(alertes)
			for sensors in alertes[alerte]:
				#print(sensors)
				parametre = alertes[alerte][sensors]
				#print(parametre)
				groupes.setdefault(alerte, []).append({sensors: alertes[alerte][sensors]})  # Regroupement par paramètre
	
		# Style pour les en-têtes de section
		style = ttk.Style()
		style.configure("Groupe.TLabel", font=('Arial', 12, 'bold'), background="#CDCDB4", foreground="#303030")
	
		# Affichage des alertes groupées et triées
		for date_heure_minute in sorted(groupes.keys(), key=lambda x: datetime.strptime(x, "%d %B %Y %I:%M%p"), reverse=True):
			alertes_triees = groupes[date_heure_minute]
			#print(alertes_triees)
			ttk.Label(scrollable_frame, text=f"Alertes {date_heure_minute.capitalize()} :", style="Groupe.TLabel").pack(fill="x", padx=10, pady=(15, 5))
	
			for alerte_par_parametres in alertes_triees:
				for parametres in alerte_par_parametres:
					# En-tête de section avec couleur beige
					# Tri des alertes par date (récent -> ancien)
					# print(parametres)
					# print(date_heure_minute)
					# print(alerte_par_parametres)
					date_formatee = datetime.strptime(date_heure_minute, "%d %B %Y %I:%M%p").strftime("%d %B %Y %I:%M%p")
					texte = f"• {alerte_par_parametres[parametres]['valeur']}{unite(parametres)} - {alerte_par_parametres[parametres]['message']}"
					# Label avec fond gris et texte clair
					ttk.Label(scrollable_frame, text=texte, background="#303030", foreground="white", padding=(20, 5)).pack(fill="x", padx=20)
	
		# Mise à jour finale de l'affichage
		scrollable_frame.update_idletasks()
		canvas.configure(scrollregion=canvas.bbox("all"))
		return fenetre
	else:
		for alerte in alertes:
			if alertes_date in alerte:
				for sensors in alertes[alerte]:
					if alertes_param in sensors:
						groupes.setdefault(alerte, []).append({sensors: alertes[alerte][sensors]})  # Regroupement par paramètre

		# Style pour les en-têtes de section
		style = ttk.Style()
		style.configure("Groupe.TLabel", font=('Arial', 12, 'bold'), background="#CDCDB4", foreground="#303030")

		# Affichage des alertes groupées et triées
		for date_heure_minute in sorted(groupes.keys(), key=lambda x: datetime.strptime(x, "%d %B %Y %I:%M%p"),
										reverse=True):
			alertes_triees = groupes[date_heure_minute]
			# print(alertes_triees)
			ttk.Label(scrollable_frame, text=f"Alertes {date_heure_minute.capitalize()} :",
					  style="Groupe.TLabel").pack(fill="x", padx=10, pady=(15, 5))

			for alerte_par_parametres in alertes_triees:
				for parametres in alerte_par_parametres:
					# En-tête de section avec couleur beige
					# Tri des alertes par date (récent -> ancien)
					# print(parametres)
					# print(date_heure_minute)
					# print(alerte_par_parametres)
					date_formatee = datetime.strptime(date_heure_minute, "%d %B %Y %I:%M%p").strftime("%d %B %Y %I:%M%p")
					texte = f"• {alerte_par_parametres[parametres]['valeur']}{unite(parametres)} - {alerte_par_parametres[parametres]['message']}"
					# Label avec fond gris et texte clair
					ttk.Label(scrollable_frame, text=texte, background="#303030", foreground="white", padding=(20, 5)).pack(fill="x", padx=20)

		# Mise à jour finale de l'affichage
		scrollable_frame.update_idletasks()
		canvas.configure(scrollregion=canvas.bbox("all"))
		return fenetre

def get_problem_trolololo(alertes_param, alertes_date):
	# Chargement des données depuis le fichier JSON
	alertes = open_data("alertes.json")
	seuil = open_data("optimal_threshold.json")
	groupes = {}

	list_tally = {}
	for param in seuil:
		list_tally[param] = 0
		# print(alerte)
		# print(alertes)
		for dates in alertes:
			if alertes_date in dates:
				for parametre in alertes[dates]:
					if param == parametre:
						list_tally[param] += 1


	if (list_tally["Température"] > list_tally["Humidité"]) and (list_tally["Température"] > list_tally["CO2"]) and (list_tally["Température"] > list_tally["Lumière"]):
		return "Température"
	elif (list_tally["Humidité"] > list_tally["Température"]) and (list_tally["Humidité"] > list_tally["CO2"]) and (list_tally["Humidité"] > list_tally["Lumière"]):
		return "Humidité"
	elif (list_tally["CO2"] > list_tally["Température"]) and (list_tally["CO2"] > list_tally["Humidité"]) and (list_tally["CO2"] > list_tally["Lumière"]):
		return "CO2"
	elif (list_tally["Lumière"] > list_tally["Température"]) and (list_tally["Lumière"] > list_tally["Humidité"]) and (list_tally["Lumière"] > list_tally["CO2"]):
		return "Lumière"
	else:
		return "aucun paramètre"




def unite(parametre):
	# Dictionnaire des unités de mesure
	return {"Température": "°C", "Humidité": "%", "CO2": " ppm", "Lumière": " lux"}.get(parametre, "")

def nombre_alertes():
	toute_les_alertes = open_data("alertes.json")
	nb_alertes = 0
	for alertes in toute_les_alertes:
		for parametre in toute_les_alertes[alertes]:
			if (toute_les_alertes[alertes][parametre]["status"] == "active"):
				nb_alertes += 1
				#print(toute_les_alertes)
				#print(alertes)
				#print(parametre)
	return nb_alertes

if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	creer_fenetre_alertes()
	root.mainloop()










