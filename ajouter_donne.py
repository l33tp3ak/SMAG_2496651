import tkinter as tk
import datetime
import calendar
from tkinter import ttk, messagebox
import add_data
from chargement import open_data, write_data

def ajoute_donne(main_frame):
	# On détruit tous les widgets précédemment placés dans main_frame
	for widget in main_frame.winfo_children():
		widget.destroy()

	# Titre principal
	tk.Label(main_frame, text="Ajouter les données", font=("Arial", 16, "bold"), bg="#303030", fg="#ffffff").pack(pady=10, fill=tk.X)

	# Cadre principal qui contient deux sous-cadres
	top_frame = tk.Frame(main_frame, bg="#CDCDB4", relief=tk.GROOVE, borderwidth=2)
	top_frame.pack(fill=tk.X, padx=10, pady=10)

	# ==================== PARTIE GAUCHE : SAISIE DE LA DATE & HEURE ====================
	top_frame_gauche = tk.Frame(top_frame, bg="#8B8B7A")
	top_frame_gauche.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

	tk.Label(top_frame_gauche, text="Jour", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=0, padx=5, pady=2)
	tk.Label(top_frame_gauche, text="Mois", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=1, padx=5, pady=2)
	tk.Label(top_frame_gauche, text="Année", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=2, padx=5, pady=2)

	# Combobox pour la sélection du jour, du mois et de l'année
	jour_combo = ttk.Combobox(top_frame_gauche, values=[str(i).zfill(2) for i in range(1, 32)], width=4, state="readonly")
	jour_combo.set(datetime.datetime.now().strftime("%d"))
	mois_combo = ttk.Combobox(top_frame_gauche, values=[str(i).zfill(2) for i in calendar.month_name[1:]], width=10, state="readonly")
	mois_combo.set(datetime.datetime.now().strftime("%B"))
	annee_combo = ttk.Combobox(top_frame_gauche, values=[str(i) for i in range(2020, 2030)], width=6, state="readonly")
	# Non-fonctionnel du au difference entre datetime et la structure des indice
	annee_combo.set(datetime.datetime.now().strftime("%Y"))

	jour_combo.grid(row=1, column=0, padx=5, pady=2)
	mois_combo.grid(row=1, column=1, padx=5, pady=2)
	annee_combo.grid(row=1, column=2, padx=5, pady=2)

	# Ajout d'un label et d'une entry pour l'heure
	ampm_valeur = ("AM","PM")
	tk.Label(top_frame_gauche, text="Heure (HH:MM)", font=("Arial", 10), bg="#8B8B7A").grid(row=2, column=0, columnspan=2, padx=5, pady=5)
	heure_entry = ttk.Entry(top_frame_gauche, width=10)
	heure_entry.grid(row=2, column=2, padx=5, pady=5)
	# Donne la valeur par defaut pour l'heure
	heure_entry.insert(0, datetime.datetime.now().strftime("%I:%M"))  # Valeur par défaut
	ampm_combo = ttk.Combobox(top_frame_gauche, values=[str(i).zfill(2) for i in ampm_valeur], width=6, state="readonly")
	ampm_combo.set(datetime.datetime.now().strftime("%p"))
	ampm_combo.grid(row=2, column=3, padx=5, pady=5)

	# ==================== PARTIE DROITE : SAISIE DES PARAMÈTRES CAPTEURS ====================
	# Crée les variable booléenne représentant nos checkbox avec une valeur "True", soit sélectionnée, par défaut.
	temp_check_bool, humidite_check_bool, lumiere_check_bool, co2_check_bool = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True)
	top_frame_droite = tk.Frame(top_frame, bg="#AAAAAA")
	top_frame_droite.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

	tk.Label(top_frame_droite, text="Température (°C)", font=("Arial", 10), bg="#AAAAAA").grid(row=0, column=0, padx=5, pady=5, sticky="e")
	temperature_entry = ttk.Entry(top_frame_droite, width=10)
	temperature_entry.grid(row=0, column=1, padx=5, pady=5)
	temp_check = ttk.Checkbutton(top_frame_droite, onvalue=True, offvalue=False, variable=temp_check_bool)
	temp_check.grid(row=0, column=2, padx=0, pady=0)

	tk.Label(top_frame_droite, text="Humidité (%)", font=("Arial", 10), bg="#AAAAAA").grid(row=1, column=0, padx=5, pady=5, sticky="e")
	humidite_entry = ttk.Entry(top_frame_droite, width=10)
	humidite_entry.grid(row=1, column=1, padx=5, pady=5)
	humidite_check = ttk.Checkbutton(top_frame_droite, onvalue=True, offvalue=False, variable=humidite_check_bool)
	humidite_check.grid(row=1, column=2, padx=0, pady=0)

	tk.Label(top_frame_droite, text="Lumière (lux)", font=("Arial", 10), bg="#AAAAAA").grid(row=2, column=0, padx=5, pady=5, sticky="e")
	lumiere_entry = ttk.Entry(top_frame_droite, width=10)
	lumiere_entry.grid(row=2, column=1, padx=5, pady=5)
	lumiere_check = ttk.Checkbutton(top_frame_droite, onvalue=True, offvalue=False, variable=lumiere_check_bool)
	lumiere_check.grid(row=2, column=2, padx=0, pady=0)


	tk.Label(top_frame_droite, text="CO2 (ppm)", font=("Arial", 10), bg="#AAAAAA").grid(row=3, column=0, padx=5, pady=5, sticky="e")
	co2_entry = ttk.Entry(top_frame_droite, width=10)
	co2_entry.grid(row=3, column=1, padx=5, pady=5)
	co2_check = ttk.Checkbutton(top_frame_droite, onvalue=True, offvalue=False, variable=co2_check_bool)
	co2_check.grid(row=3, column=2, padx=0, pady=0)

	# Création du cadre en bas pour afficher les données
	bottom_frame = tk.Frame(main_frame, bg="#303030")
	bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

	# ==================== FONCTION DE VALIDATION ====================
	def on_button_click():
		# --- Récupération des valeurs de date/heure ---
		day = jour_combo.get()
		month = mois_combo.get()
		year = annee_combo.get()
		time_choisi = f"{heure_entry.get().strip()}{ampm_combo.get()}"
		selected_parametres = ({"Température": temp_check_bool.get()}, {"Humidité": humidite_check_bool.get()}, {"Lumière": lumiere_check_bool.get()}, {"CO2": co2_check_bool.get()})
		parametre_values = {
			"Température": temperature_entry.get().strip(),
			"Humidité": humidite_entry.get().strip(),
			"Lumière": lumiere_entry.get().strip(),
			"CO2": co2_entry.get().strip()
		}

		for parametre in parametre_values:
			if (parametre_values[parametre] != None) and (parametre_values[parametre] != ""):
				try:
					parametre_values[parametre] = float(parametre_values[parametre])
				except ValueError:
					messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour les capteurs.")
					return


		# --- Construction de la date et heure finale ---
		time = f"{day} {month} {year} {time_choisi}"

		# --- Récupération et vérification des paramètres environnementaux ---
		for parametre in selected_parametres:
			for nom_parametre in parametre:
				if parametre[nom_parametre]:
					if (parametre_values[nom_parametre] == None or parametre_values[nom_parametre] == ""):
						add_data.struct_sensor_data(nom_parametre, time)
					else:
						add_data.struct_sensor_data(nom_parametre, time, parametre_values[nom_parametre])



		messagebox.showinfo("Succès", f"Données enregistrées pour la date : {time}")

		# Réinitialisation des champs
		jour_combo.set("")
		jour_combo.current(int(datetime.datetime.now().strftime("%d")))
		mois_combo.set("")
		mois_combo.current(int(datetime.datetime.now().strftime("%m")) - 1)
		annee_combo.set(datetime.datetime.now().strftime("%Y"))
		heure_entry.delete(0, tk.END)
		heure_entry.insert(0, datetime.datetime.now().strftime("%I:%M"))
		temperature_entry.delete(0, tk.END)
		humidite_entry.delete(0, tk.END)
		lumiere_entry.delete(0, tk.END)
		co2_entry.delete(0, tk.END)



	# Fonction pour générer des données aléatoires à la date sélectionnée
	def generer_donnees_aleatoires():

		selected_date = f"{annee_combo.get()}-{mois_combo.get()}-{jour_combo.get()}"

		# Générer les données
		add_data.auto_sensor_data()
		messagebox.showinfo("Succès", f"8 mesures générées avec succès pour la date du {selected_date}!")

		# Réinitialiser les combobox
		jour_combo.set("")
		mois_combo.set("")
		annee_combo.set("")

	# ==================== BOUTONS ====================
	# Bouton pour l'ajout manuel
	bouton_valider = tk.Button(main_frame,text="Enregistrer les données des capteurs",font=("Arial", 12, "bold"),bg="#4CAF50",fg="#FFFFFF",command=on_button_click)
	bouton_valider.pack(pady=5)

	"""# Bouton pour générer des données aléatoires
	bouton_aleatoire = tk.Button(main_frame,text="Générer 8 mesures aléatoires",font=("Arial", 12, "bold"),bg="#4169E1",fg="#FFFFFF",command=generer_donnees_aleatoires)
	bouton_aleatoire.pack(pady=5)

	# Texte explicatif pour la génération aléatoire
	tk.Label(main_frame,text="Note: La génération aléatoire créera 8 mesures espacées de 3 heures\nà partir de minuit pour la date sélectionnée.",font=("Arial", 10),bg="#303030",fg="#ffffff").pack(pady=5)"""



