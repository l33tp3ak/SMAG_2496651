import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from chargement import open_env_data

"""
Ici, le problème est que, auparavant, dans mon fichier, je pouvais sélectionner une seule date, et la date était dans un fichier 
où les heures et les dates étaient séparées : la date à l'index et l'heure une donnée. Donc, il faut que je trouve une solution pour 
afficher le graphique de toutes les heures d'une même journée.
"""
# --------------------------- PARTIE 1 : INTERFACE PRINCIPALE ---------------------------
def afficher_menu_tendances(parent_frame):
    # Nettoyage du frame parent
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Création du frame principal
    frame_principale = tk.Frame(parent_frame, bg="#CDCDB4", relief=tk.GROOVE, borderwidth=2)
    frame_principale.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Titre
    tk.Label(frame_principale, text="Tendances Moyennes en Date du :", font=("Arial", 16, "bold"), bg="#CDCDB4").pack(pady=10)
    
    # Frame supérieur pour les trois sections
    top_frame = tk.Frame(frame_principale, bg="#8B8B7A")
    top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # 1.2 SECTION GAUCHE : COMBOBOX, SELECTEUR DATE  ---------------------------
    frame_gauche = tk.Frame(top_frame, bg="#8B8B7A")
    frame_gauche.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    # Labels pour les sélecteurs de date dans SECTION GAUCHE
    tk.Label(frame_gauche, text="Jour", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=0, padx=5, pady=2)
    tk.Label(frame_gauche, text="Mois", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=1, padx=5, pady=2)
    tk.Label(frame_gauche, text="Année", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=2, padx=5, pady=2)
    
    # Combobox pour la sélection de la date SECTION GAUCHE en desssou des label avec une boucle qui s'assure que tout les nombre a moin de 2 chifre commence par un zero
    mois_de_annee = ("Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre")
    # Combobox pour la sélection de la date SECTION GAUCHE en desssou des label avec une boucle qui s'assure que tout les nombre a moin de 2 chifre commence par un zero
    jour_combo = ttk.Combobox(frame_gauche, values=[str(i).zfill(2) for i in range(1, 32)], width=4, state="readonly")
    mois_combo = ttk.Combobox(frame_gauche, values=[str(i).zfill(2) for i in mois_de_annee], width=6, state="readonly")
    annee_combo = ttk.Combobox(frame_gauche, values=[str(i) for i in range(2020, 2026)], width=6, state="readonly")

    jour_combo.grid(row=1, column=0, padx=5, pady=2)
    mois_combo.grid(row=1, column=1, padx=5, pady=2)
    annee_combo.grid(row=1, column=2, padx=5, pady=2)

    # Bouton "Afficher" SECTION GAUCHE en dessous des Combobox SECTION GAUCHE
    def on_button_click():
        day = jour_combo.get()    # Ex: "01"
        month = mois_combo.get()  # Ex: "Decembre"
        year = annee_combo.get()  # Ex: "2024"

        if not day or not month or not year:
            messagebox.showwarning("Erreur", "Veuillez sélectionner une date complète.")
            return

        # Construire la date au format JSON sans l'heure
        date_choisi = f"{year}-{month}-{day}"
        print(f"Date choisie : {date_choisi}")  # 🔍 Vérification 1

        # Charger le fichier JSON
        data = open_env_data("environment.json")
        print("Données JSON chargées :", data)  # 🔍 Vérification 2

        # Filtrer les entrées qui commencent par cette date
        print("Filtrage des entrées...")
        filtered_data = [entry for entry in data if entry["Date"].startswith(date_choisi)]
        print("Données après filtrage :", filtered_data)  # 🔍 Vérification 3

        if not filtered_data:
            messagebox.showwarning("Erreur", f"Aucune donnée disponible pour la date {date_choisi}.")
            return

        # Mettre à jour l'affichage des moyennes
        latest_entry = filtered_data[-1]  # Prendre la dernière entrée du jour
        nom_des_parametre["date"].config(text=f"Date : {latest_entry['Date']}")
        nom_des_parametre["temp"].config(text=f"Température : {latest_entry['Température']} °C")
        nom_des_parametre["humidity"].config(text=f"Humidité : {latest_entry['Humidité']} %")
        nom_des_parametre["co2"].config(text=f"CO2 : {latest_entry['CO2']} ppm")

        # Récupérer le paramètre choisi pour le graphique
        parametre_choisi = parameter_combox.get()

        # Afficher le graphique avec toutes les valeurs de cette journée
        tracer_graphique(parametre_choisi, frame_du_bas, filtered_data)


        """
        1. met à jour les labels de l'interface graphique avec les données environnementales (température, humidité, CO2) pour la date sélectionnée.
           Elle utilise le backend pour récupérer les données et les afficher dans les labels (nom_des_parametre).
            
        2. Récupère le paramètre choisi par l'utilisateur dans la Combobox (température, humidité ou CO2).
           Ce paramètre détermine quel graphique sera affiché.

        3. Trace un graphique dans le (frame_du_bas) pour le paramètre choisi et la date sélectionnée.
           Le graphique montre l'évolution du paramètre (ex: température) au cours de la journée.
        """
       # open_env_data.update_moyenne(date_choisi, nom_des_parametre)# 1**
       # parametre_choisi = parameter_combox.get()# 2**
       # tracer_graphique(parametre_choisi, frame_du_bas, date_choisi)# 3**

    # Création du bouton "Afficher" et placement dans la grille
    ttk.Button(frame_gauche, text="Afficher", command=on_button_click).grid(row=2, column=0, columnspan=3, pady=10)


    # 1.3 SECTION AU CENTRE: VALEURS ENVIRONNEMENTALES ---------------------------
    frame_du_centre = tk.Frame(top_frame, bg="#8B8B7A", relief=tk.GROOVE, borderwidth=2)
    frame_du_centre.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Création des labels pour les paramètres
    nom_des_parametre = {
        "date": tk.Label(frame_du_centre, text="Date : ", font=("Arial", 12), bg="#8B8B7A"),
        "temp": tk.Label(frame_du_centre, text="Température :", font=("Arial", 12), bg="#8B8B7A"),
        "humidity": tk.Label(frame_du_centre, text="Humidité : ", font=("Arial", 12), bg="#8B8B7A"),
        "co2": tk.Label(frame_du_centre, text="CO2 :", font=("Arial", 12), bg="#8B8B7A")
    }

    # Placement des labels
    nom_des_parametre["date"].grid(row=0, column=0, sticky="w", padx=10, pady=5)
    nom_des_parametre["temp"].grid(row=1, column=0, sticky="w", padx=60, pady=5)
    nom_des_parametre["humidity"].grid(row=2, column=0, sticky="w", padx=60, pady=5)
    nom_des_parametre["co2"].grid(row=3, column=0, sticky="w", padx=60, pady=5)

    # 1.4 SECTION DROITE : CONDITIONS OPTIMALES ---------------------------
    frame_droite = tk.Frame(top_frame, bg="palegreen", relief=tk.GROOVE, borderwidth=2)
    frame_droite.pack(side=tk.RIGHT, padx=10)

    tk.Label(frame_droite, text="Conditions Optimales", font=("Arial", 14), bg="palegreen").pack(pady=5)
    tk.Label(frame_droite, text="Température : 20-25°C", font=("Arial", 12), bg="palegreen").pack(pady=2)
    tk.Label(frame_droite, text="Humidité : 50-70%", font=("Arial", 12), bg="palegreen").pack(pady=2)
    tk.Label(frame_droite, text="CO2 : 350-450 ppm", font=("Arial", 12), bg="palegreen").pack(pady=2)

    # 1.5 cree un nouveau frame pour ajouter le widget combobox du selecteur de parametre Sélecteur de paramètre pour choisir le graphique à afficher -----
    frame_parametre = tk.Frame(frame_principale, bg="lightyellow")
    frame_parametre.pack(pady=5)

    tk.Label(frame_parametre, text="Paramètre :", font=("Arial", 12), bg="lightyellow").pack(side=tk.LEFT, padx=5)
    # 
    parameter_combox = ttk.Combobox(frame_parametre, values=["Température", "Humidité", "CO2"], state="readonly")
    parameter_combox.set("Température")
    parameter_combox.pack(side=tk.LEFT, padx=5)

    # 1.6 Frame du graphique en bas ------------------------
    frame_du_bas = tk.Frame(frame_principale, bg="white", height=400)
    frame_du_bas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

# - "<<ComboboxSelected>>" : Événement déclenché lorsque l'utilisateur sélectionne une nouvelle option dans la Combobox.
# - lambda _: on_parameter_selected(...) : Fonction anonyme qui appelle on_parameter_selected avec les arguments suivants :
#   - parameter_combox.get() : Récupère la valeur actuellement sélectionnée dans la Combobox (ex: "Température").
#   - nom_des_parametre : Dictionnaire contenant les labels des paramètres (date, température, humidité, CO2).
#   - frame_du_bas : Frame où le graphique est affiché.
    parameter_combox.bind("<<ComboboxSelected>>", lambda _: on_parameter_selected(parameter_combox.get(), nom_des_parametre, frame_du_bas))

# --------------------------- PARTIE 2 : GESTION DU CHANGEMENT DE PARAMÈTRE ---------------------------
def on_parameter_selected(selected_parameter, nom_des_parametre, frame_du_bas): #selected_parameter = parameter_combox.get()
    """
    Fonction appelée lorsque l'utilisateur change le paramètre à afficher dans le graphique.
    - selected_parameter : Le paramètre sélectionné dans la Combobox (ex: "Température").
    - nom_des_parametre : Dictionnaire contenant les labels des paramètres (date, température, humidité, CO2).
    - frame_du_bas : Frame où le graphique est affiché.
    """
    if "date" in nom_des_parametre:
        try:
            # Récupère la date à partir du texte du label "date"
            selected_date = nom_des_parametre["date"].cget("text").split(": ")[1]
        except IndexError:
            selected_date = None
    else:
        # Si la clé "date" n'existe pas, selected_date est défini à None
        selected_date = None

    # Si une date valide est disponible, trace le graphique en apellant la fonction tracer_graphique
    if selected_date:
        tracer_graphique(selected_parameter, frame_du_bas, selected_date)

# --------------------------- PARTIE 3 : TRACER LE GRAPHIQUE ---------------------------
def tracer_graphique(parameter, frame, date):
    detailed_data = open_env_data.get_detailed_trend_data(date)
    
    if not detailed_data:
        messagebox.showwarning("Erreur", f"Aucune donnée disponible pour la date {date}.")
        return

    # Conversion des clés si nécessaire (ex: "Température" -> "température")
    parameter_key = {
        "Température": "Température",
        "Humidité": "Humidité", 
        "CO2": "CO2"
    }[parameter]

    hours = list(detailed_data.keys())
    values = [detailed_data[hour][parameter_key] for hour in hours]
    
    # ... (reste du code inchangé)

    for widget in frame.winfo_children():
        widget.destroy()

    ## Crée une figure et des axes pour le graphique
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(hours, values, marker='o', color='blue', label=parameter)
    ax.set_title(f"Évolution de {parameter} - {date}", fontsize=14)
    ax.set_xlabel("Heures")
    ax.set_ylabel(parameter)
    ax.grid(True)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --------------------------- MAIN ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion de la Serre Intelligente")
    root.geometry("1200x750")
    afficher_menu_tendances(root)
    root.mainloop()