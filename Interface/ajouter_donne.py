import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
#from backend_ import param_enviro, sauvegarder_param_enviro


def ajoute_donne(main_frame):
    # On détruit tous les widgets précédemment placés dans main_frame.
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Titre principal
    tk.Label(main_frame, text="Ajouter les données", font=("Arial", 16, "bold"), bg="#303030", fg="#ffffff").pack(pady=10, fill=tk.X)

    # Cadre principal qui contient deux sous-cadres: un pour la DATE/HEURE (à gauche), un pour les VALEURS CAPTEURS (à droite)
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
    mois_combo = ttk.Combobox(top_frame_gauche, values=[str(i).zfill(2) for i in range(1, 13)], width=6, state="readonly")
    annee_combo = ttk.Combobox(top_frame_gauche, values=[str(i) for i in range(2020, 2030)], width=6, state="readonly")

    jour_combo.grid(row=1, column=0, padx=5, pady=2)
    mois_combo.grid(row=1, column=1, padx=5, pady=2)
    annee_combo.grid(row=1, column=2, padx=5, pady=2)

    # Ajout d'un label et d'une combobox/Entry pour l'heure
    tk.Label(top_frame_gauche, text="Heure (HH:MM)", font=("Arial", 10), bg="#8B8B7A").grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    heure_entry = ttk.Entry(top_frame_gauche, width=10)
    heure_entry.grid(row=2, column=2, padx=5, pady=5)
    heure_entry.insert(0, "08:00")  # Valeur par défaut

    # ==================== PARTIE DROITE : SAISIE DES PARAMÈTRES CAPTEURS ====================
    top_frame_droite = tk.Frame(top_frame, bg="#AAAAAA")
    top_frame_droite.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    tk.Label(top_frame_droite, text="Température (°C)", font=("Arial", 10), bg="#AAAAAA").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    temperature_entry = ttk.Entry(top_frame_droite, width=10)
    temperature_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(top_frame_droite, text="Humidité (%)", font=("Arial", 10), bg="#AAAAAA").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    humidite_entry = ttk.Entry(top_frame_droite, width=10)
    humidite_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(top_frame_droite, text="Lumière (lux)", font=("Arial", 10), bg="#AAAAAA").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    lumiere_entry = ttk.Entry(top_frame_droite, width=10)
    lumiere_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(top_frame_droite, text="CO2 (ppm)", font=("Arial", 10), bg="#AAAAAA").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    co2_entry = ttk.Entry(top_frame_droite, width=10)
    co2_entry.grid(row=3, column=1, padx=5, pady=5)

     # Création du cadre en bas pour afficher les données
    bottom_frame = tk.Frame(main_frame, bg="#303030")
    bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Appel de la fonction pour afficher les données
   # afficher_dernieres_donnees(bottom_frame)

    # ==================== FONCTION DE VALIDATION ====================
    def on_button_click():
        # --- Récupération des valeurs de date/heure ---
        day = jour_combo.get()
        month = mois_combo.get()
        year = annee_combo.get()
        time_choisi = heure_entry.get().strip()

        # Vérification que la date est complète
        if not day or not month or not year:
            messagebox.showwarning("Erreur", "Veuillez sélectionner une date complète.")
            return

        # --- Construction de la date et heure finale ---
        # Ex: "2024-12-01 08:00"
        date_heure_choisie = f"{year}-{month}-{day} {time_choisi}"

        # --- Récupération des paramètres environnementaux ---
        try:
            temperature = float(temperature_entry.get().strip())
            humidite = float(humidite_entry.get().strip())
            lumiere = float(lumiere_entry.get().strip())
            co2 = float(co2_entry.get().strip())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques pour les capteurs.")
            return

        # Exemple de dictionnaire qu’on veut ajouter
        nouvelle_entree = {
            "Date": date_heure_choisie,
            "Température": temperature,
            "Humidité": humidite,
            "Lumière": lumiere,
            "CO2": co2
        }
""""
   # Déléguer le traitement à une fonction de logique
    try:
        traiter_et_sauvegarder_donnees(nouvelle_entree)
        messagebox.showinfo("Succès", f"Données enregistrées pour la date : {date_heure_choisie}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de traiter les données : {e}")

    # Réinitialisation des champs
    jour_combo.set("")
    mois_combo.set("")
    annee_combo.set("")
    heure_entry.delete(0, tk.END)
    heure_entry.insert(0, "08:00")
    temperature_entry.delete(0, tk.END)
    humidite_entry.delete(0, tk.END)
    lumiere_entry.delete(0, tk.END)
    co2_entry.delete(0, tk.END)

    # ==================== BOUTON DE VALIDATION ====================
    bouton_valider = tk.Button(main_frame, text="Enregistrer les données", font=("Arial", 12, "bold"), bg="#4CAF50", fg="#FFFFFF", command=on_button_click); bouton_valider.pack(pady=10)


#    Ici je dois importer la fonction qui read le fichier json  (((donnees = param_enviro())))
def afficher_dernieres_donnees(bottom_frame):

    # Charger les données depuis la fonction backend
    donnees = param_enviro()

    # Trier par date décroissante
    donnees_triees = sorted(donnees, key=lambda x: datetime.strptime(x["Date"], "%Y-%m-%d %H:%M"), reverse=True)

    # Prendre les 5 dernières données
    dernieres_donnees = donnees_triees[:5]

    # Effacer les anciens widgets
    for widget in bottom_frame.winfo_children():
        widget.destroy()

    # Ajouter un titre
    tk.Label(bottom_frame, text="5 dernières données enregistrées", font=("Arial", 12, "bold"), bg="#303030", fg="#FFFFFF").pack(pady=5)

    # Afficher chaque donnée
    for entree in dernieres_donnees:
        texte = f"{entree['Date']} | Temp: {entree['Température']}°C | Hum: {entree['Humidité']}% | Lum: {entree['Lumière']} lux | CO2: {entree['CO2']} ppm"
        tk.Label(bottom_frame, text=texte, font=("Arial", 10), bg="#F0F0F0", anchor="w").pack(fill=tk.X, padx=5, pady=2)

"""