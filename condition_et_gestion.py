import json
import tkinter as tk
# Bibliothèques nécessaires aux jauges circulaires
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from chargement import open_env_data 
# Fonction pour obtenir les conditions simulées


# ----------------------------- PARTIE 1 : Création DU TOP FRAME -------------------------------
"""
     - Séparer le top_frame en deux frames (gauche et droite).
     - top_frame_gauche : contient la grille de paramètres et des conditions actuelles.
     - top_frame_droite : contient 3 "boutons de volume" (ici, des tk.Scale)
       pour Irrigation, Lumière et Ventilation avec 4 niveaux (0,1,2,3).
       et pour finir un graphique dynamique qui interagit avec les conditions et les paramètres.
"""
# Fonction principale pour afficher les conditions actuelles
def condition_actuelles(main_frame):
    # On détruit tous les widgets précédemment placés dans main_frame.
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Titre principal
    tk.Label(main_frame, text="Conditions Actuelles", font=("Arial", 16, "bold"), bg="#303030", fg="#ffffff").pack(pady=10, fill=tk.X)

    # Cadre supérieur global (top_frame)
    top_frame = tk.Frame(main_frame, bg="#CDCDB4", relief=tk.GROOVE, borderwidth=2)
    top_frame.pack(fill=tk.X, padx=10, pady=10)

    # -- FRAME DE GAUCHE-- dans le top_frame pour afficher les paramètres
    top_frame_gauche = tk.Frame(top_frame, bg="#8B8B7A")
    top_frame_gauche.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Charger les données depuis le fichier JSON via chargement.py
    environment_data = open_env_data("environment.json")

    # Vérification que les données sont bien chargées
    latest_entry = environment_data[-1] if environment_data else {}
    environment_data_list = {k: v for k, v in latest_entry.items() if k != "Date"}

    #On parcourt simulation_condition avec son paramètre et sa valeur, et on ajoute l'unité de mesure associée à chaque paramètre. Exemple : 'Température': '°C'.
    for i, (param, value) in enumerate(environment_data_list.items()):
        unit = {"Température": " °C", "Humidité": " %", "CO2": " ppm", "Lumière": " lux"}.get(param, "") # associer chaque paramètre (param) à son unité de mesure.
        formatted_value = f"{value}{unit}" # combine la valeur (value) et l'unité (unit) en une seule chaîne de caractères formatée.
        tk.Label(top_frame_gauche, text=f"{param} :", font=("Arial", 12), bg="#8B8B7A", anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=5)
        tk.Label(top_frame_gauche, text=formatted_value, font=("Arial", 12), bg="#CDCDB4", fg="#292421").grid(row=i, column=1, sticky="w", padx=10, pady=5)

 
    # -- FRAME DE DROITE -- pour afficher les 3 boutons/volumes
    top_frame_droite = tk.Frame(top_frame, bg="#8B8B7A")
    top_frame_droite.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
    ajouter_controles(top_frame_droite)

    # Créer les jauges
    create_jauge(main_frame)

#----------------------------------------------- PARTIE 2: les 3 boutons/volumes (dans le frame top/droite) -----------------------------------------------------------------
def ajouter_controles(frame):
    gestion = {                              # tk.IntVar : Une variable Tkinter pour stocker des entiers. Quand l'utilisateur déplace le curseur du Scale, la valeur du widget est automatiquement mise à jour.
        "Ventilation": tk.IntVar(value=0),  # 0: Off, 1: Low, 2: Medium, 3: High
        "Irrigation": tk.IntVar(value=0),  # 0: Off, 1: Low, 2: Medium, 3: High
        "Lumière": tk.IntVar(value=0)       # 0: Off, 1: Low, 2: Medium, 3: High
    }

    # Fonction pour mettre à jour l'affichage des contrôles
    def update_control(param, value):
        status = {0: "Off", 1: "Low", 2: "Medium", 3: "High"}.get(value, "Unknown")
        print(f"{param} réglé à {status}")
        # Ici,  ajouter du code pour gérer les actions réelles liées aux contrôles

    # Création des échelles pour les contrôles. La boucle parcourt chaque élément du dictionnaire pour créer un widget Scale (un curseur horizontal) pour chaque paramètre.
    for param, value in gestion.items():
        scale = tk.Scale(frame, from_=0, to=3, orient=tk.HORIZONTAL, label=param, bg="#8B8B7A", fg="#000000", troughcolor="#D0D0D0", highlightthickness=0, variable=value, command=lambda val, c=param: update_control(c, int(val)))
        scale.pack(padx=10, pady=10, fill=tk.X)

# ------------------------------------------------------- PARTIE 3 : Fonction pour créer les jauges dans Frame/en bas -----------------------------------------------------------------------------------------------
def create_jauge(bottom_frame):
    # Cadre pour le graphique
    graph_frame = tk.Frame(bottom_frame, bg="lightgrey", relief=tk.GROOVE, borderwidth=2)
    graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    gauges_frame = tk.Frame(graph_frame, bg="#1E1E1E")
    gauges_frame.pack(fill=tk.X, padx=20, pady=20)
   
    environment_data = open_env_data("environment.json")
    latest_entry = environment_data[-1] if environment_data else {}
    environment_data_list = {k: v for k, v in latest_entry.items() if k != "Date"}
    
    jauge(gauges_frame, "Température", environment_data_list["Température"], 10, 40, COLORS["temp"], "°C")  #<-------------- # Appel de la fonction jauge() pour créer une jauge 
    jauge(gauges_frame, "Humidité", environment_data_list["Humidité"], 10, 100, COLORS["humidity"], "%")                      # La fonction jauge() est définie avec les paramètres suivants :
    jauge(gauges_frame, "CO2", environment_data_list["CO2"], 111, 1100, COLORS["co2"], "ppm")                                 # frame : Le conteneur parent dans lequel la jauge sera placée (ici, gauges_frame)
                                                                                                                            # - title : Le titre de la jauge (ici, ",Température, Humidité, CO2 ").
                                                                                                                            # - value : La valeur actuelle à afficher ()
                                                                                                                            # - min_val : La valeur minimale de la jauge exemple temperature (ici,15 ).
                                                                                                                            # - max_val : La valeur maximale de la jaugeexemple temperature (ici,35 ).
                                                                                                                            # - colors : Les couleurs à utiliser pour la jauge (ici, COLORS["temp"])
                                                                                                                            # - unit : L'unité de la valeur (ici, "°C").
  # ------------------------- PARTIE 4 : Création d'une jauge circulaire interactive ------- ---                                                                                                                                          
                                                                                                                            # Lorsque la fonction jauge() est appelée, les arguments passés sont associés
def jauge(frame, title, value, min_val, max_val, colors, unit=""):        #<---------------------------------------------   # aux paramètres de la fonction dans l'ordre où ils sont définis.
    #  Frame 
    gauge_frame = tk.Frame(frame, bg="#1E1E1E")
    gauge_frame.pack(pady=10, padx=10, side=tk.LEFT)

    # Création d'une figure matplotlib "en polar" = (jauge circulaire)
    fig, ax = plt.subplots(figsize=(3.5, 3.5), subplot_kw={'projection': 'polar'})    # fig = Dimenssion et ax = forme
    fig.patch.set_facecolor('#1E1E1E')  # Couleur de fond de la figure
    ax.set_facecolor('#1E1E1E')         # Couleur de fond de la zone de tracé

    # value
    value_num = float(value)

    # On crée une série d'angles pour tracer des arcs colorés, len(colors) va compté le nombre de couleur pour cree les angle 
    angles = np.linspace(0, 240, len(colors))
    angles = np.deg2rad(angles)  # Conversion degrés -> radians pour donner forme au cercle en dégrader

     # **** cettte boucle me permet d'ajouter et enlever des couleur sans que cela cause probleme 
    for i in range(len(colors) - 1): 
        ax.fill_between([angles[i], angles[i+1]], 0.4, 1.2, #  À chaque itération, elle trace un arc entre angles[i] et angles[i+1] . détermine la grosseur de l'angle (couleur) dans le cercle 
                        color=colors[i], alpha=0.3)                                                       # supérieur et inférieur  

    # Placement des "ticks" (graduations) de 0 à 240°, ici on en met 
    tick_angles = np.linspace(0, 240, 10)  # angles en degrés de 0 a 240 bon de 10
    tick_values = np.linspace(min_val, max_val, 10)
    ax.set_xticks(np.deg2rad(tick_angles)) #Convertit les angles de degrés en radians.
    ax.set_xticklabels([f'{int(v)}' for v in tick_values], color='white') #****Cette ligne définit les étiquettes (labels) à afficher à chaque graduation.

    # Calcul de l'angle de l'aiguille selon la proportion
    #L'angle 0° correspond à la valeur minimale (min_val)
    #L'angle 240° correspond à la valeur maximale (max_val).
    #L'aiguille doit pointer vers la valeur actuelle (value_num).
    needle_angle = 240 * (value_num - min_val) / (max_val - min_val)  # on calcule l'écart pour que l'guille ce positionne
    needle_angle = np.deg2rad(needle_angle) #Convertit les angles de degrés en radians.

    # La fonction ax.plot() est utilisée pour tracer des lignes ou des courbes sur un graphique
    ax.plot([0.5, needle_angle], [0, 0.9], color='black', linewidth=4)

    # ax.set_ylim(0, 1),  définiss que le rayon de la jauge va de 0 (centre) à 1 (bord extérieur)
    ax.set_ylim(0, 1)

    # Ajout du titre à l'intérieur de la jauge
    ax.text(
        np.deg2rad(300),  # Angle en radians (300° pour le placer en bas a droite)
        0.8,              # Rayon (position verticale, 0.5 pour le centrer)
        f"{title}\n{value}{unit}",  # Texte du titre
        color='white',    # Couleur du texte
        fontsize=9,      # Taille de la police
        ha='center',      # Alignement horizontal au centre
        va='center'       # Alignement vertical au centre
    )

    # Suppression du quadrillage et des ticks radiaux des jauges polair
    ax.grid(False)
    ax.set_rticks([])

    # On intègre la figure matplotlib dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=gauge_frame) #Cette ligne crée un canevas (canvas) qui permet d'afficher une figure Matplotlib (fig) dans une interface Tkinter
    canvas.draw()                                    # Cette ligne dessine la figure sur le canevas.
    canvas.get_tk_widget().pack()                   # convertir l'objet FigureCanvasTkAgg en un widget Tkinter

    return gauge_frame

# Dictionnaire global pour les couleurs des jauges
COLORS = {
    "temp": ['white', 'turquoise', 'lime', 'lime', 'yellow', 'darkorange', 'red', 'red'],  # Température
    "humidity": ['white','white', 'mistyrose',  'paleturquoise', 'paleturquoise', 'dodgerblue', 'dodgerblue', 'navy'],  # Humidité
    "co2": ['white', 'whitesmoke', 'lightgray', 'silver', 'gray', 'dimgray', 'dimgray' 'black']  # CO2
}

#------------------ TEST LOCAL : si on exécute ce fichier directement-----------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test - Conditions Actuelles")
    root.geometry("1200x750")

    main_frame = tk.Frame(root, bg="silver", relief=tk.SUNKEN, borderwidth=2)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Afficher l'écran des conditions
    condition_actuelles(main_frame)

    # Boucle principale de Tkinter
    root.mainloop()