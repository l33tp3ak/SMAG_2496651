import tkinter as tk
from tkinter import ttk, messagebox
import add_data
from chargement import open_env_data, write_data
from chargement import open_env_data, write_data

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
    mois_combo = ttk.Combobox(top_frame_gauche, values=[str(i).zfill(2) for i in range(1, 13)], width=6, state="readonly")
    annee_combo = ttk.Combobox(top_frame_gauche, values=[str(i) for i in range(2020, 2030)], width=6, state="readonly")

    jour_combo.grid(row=1, column=0, padx=5, pady=2)
    mois_combo.grid(row=1, column=1, padx=5, pady=2)
    annee_combo.grid(row=1, column=2, padx=5, pady=2)

    # Ajout d'un label et d'une entry pour l'heure
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
        time = f"{year}-{month}-{day} {time_choisi}"

        # --- Récupération et vérification des paramètres environnementaux ---
        try:
            temperature = float(temperature_entry.get().strip())
            humidite = float(humidite_entry.get().strip())
            lumiere = float(lumiere_entry.get().strip())
            co2 = float(co2_entry.get().strip())

            # Création de la nouvelle mesure
            nouvelle_mesure = {
                "Date": time,
                "Température": temperature,
                "Humidité": humidite,
                "Lumière": lumiere,
                "CO2": co2
            }

            # Chargement des données existantes
            environment_data = open_env_data("environment.json")  # Plus de add_data
            environment_data.append(nouvelle_mesure)
            write_data("environment.json", environment_data)  # Utilisation directe

            # Vérification des seuils et ajout d'alertes si nécessaire
            for parametre, valeur in [
                ("Température", temperature),
                ("Humidité", humidite),
                ("Lumière", lumiere),
                ("CO2", co2)
            ]:
                if valeur < add_data.seuil[parametre]["min"] or valeur > add_data.seuil[parametre]["max"]:
                    add_data.struct_add_alerts(parametre, valeur, time)

            messagebox.showinfo("Succès", f"Données enregistrées pour la date : {time}")

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

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides pour les capteurs.")
            return

    # Fonction pour générer des données aléatoires à la date sélectionnée
    def generer_donnees_aleatoires():
        if not jour_combo.get() or not mois_combo.get() or not annee_combo.get():
            messagebox.showwarning("Erreur", "Veuillez sélectionner une date complète.")
            return
            
        selected_date = f"{annee_combo.get()}-{mois_combo.get()}-{jour_combo.get()}"
        
        # Générer les données
        add_data.auto_sensor_data(selected_date)
        messagebox.showinfo("Succès", f"8 mesures générées avec succès pour la date du {selected_date}!")
        
        # Réinitialiser les combobox
        jour_combo.set("")
        mois_combo.set("")
        annee_combo.set("")

    # ==================== BOUTONS ====================
    # Bouton pour l'ajout manuel
    bouton_valider = tk.Button(main_frame,text="Enregistrer les données",font=("Arial", 12, "bold"),bg="#4CAF50",fg="#FFFFFF",command=on_button_click)
    bouton_valider.pack(pady=5)

    # Bouton pour générer des données aléatoires
    bouton_aleatoire = tk.Button(main_frame,text="Générer 8 mesures aléatoires",font=("Arial", 12, "bold"),bg="#4169E1",fg="#FFFFFF",command=generer_donnees_aleatoires)
    bouton_aleatoire.pack(pady=5)

    # Texte explicatif pour la génération aléatoire
    tk.Label(main_frame,text="Note: La génération aléatoire créera 8 mesures espacées de 3 heures\nà partir de minuit pour la date sélectionnée.",font=("Arial", 10),bg="#303030",fg="#ffffff").pack(pady=5)


        
