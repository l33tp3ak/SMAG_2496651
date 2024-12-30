import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from pymongo import MongoClient
# from gestion_capteurs import activate_irrigation, activate_lighting, activate_ventilation    << importation du file de alex avec ces fonction


"""# Connexion à MongoDB
client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority")
db = client["SerreDB"]  # Remplacez par le nom réel de la base de données
collection = db["EnvironmentData"]  # Remplacez par le nom réel de la collection

def get_latest_environment_data():
    Récupère la dernière donnée ajoutée à la collection MongoDB
    latest_data = collection.find_one(sort=[("Date", -1)])  # Trie décroissant par date
    return latest_data"""


#  1 INTERFACE PRINCIPALE ET MENU
def main_interface():
    root = tk.Tk()
    root.title("Serre Intelligente - SMAG")   # Titre de la fenêtre
    root.geometry("1200x800")         # Dimensions de la fenêtre

    # Barre de menu en haut
    menu_bar = tk.Menu(root)  # 'menu_bar' est la variable utilisée pour créer une barre de menu principale.
                              # 'tk.Menu' est une fonction intégrée de tkinter permettant de créer un menu.
                              # Le paramètre 'root' relie la barre de menu à la fenêtre principale.
    
    # Menu alerte
    alert_menu = tk.Menu(menu_bar, tearoff=0)  # 'alert_menu' est un sous-menu attaché à 'menu_bar'.
                                              # Le paramètre 'tearoff=0' désactive l'option permettant de détacher ce menu déroulant.   
    alert_menu.add_command(label="Afficher les alertes", command=lambda: show_alerts(root, main_frame)) # Utilisation de lambda pour retarder l'appel de la fonction jusqu'au clic sur le bouton
    menu_bar.add_cascade(label="⚠ Alerte", menu=alert_menu)      # Ajout du menu alerte 

# Création d'une barre latérale pour les options supplémentaires
    sidebar = tk.Frame(root, bg="Olive Drab", width=200, relief=tk.RAISED, borderwidth=2)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Bouton pour afficher la condition actuelle
    condition_button = ttk.Button(sidebar, text="Condition Actuelle", command=lambda: display_condition_screen(main_frame))
    condition_button.pack(pady=10, padx=10, fill=tk.X)

# Bouton pour afficher la tendance
    trend_button = ttk.Button(sidebar, text="Tendance", command=lambda: display_trend_menu(main_frame))
    trend_button.pack(pady=10, padx=10, fill=tk.X)


    # Ajouter le menu à la fenêtre
    root.config(menu=menu_bar)

    # Cadre principal
    # 'main_frame' est un cadre principal avec un fond blanc, un effet 'SUNKEN', et une bordure épaisse.
     # Il est utilisé pour organiser les widgets à l'intérieur de la fenêtre principale.
    main_frame = tk.Frame(root, bg="silver", relief=tk.SUNKEN, borderwidth=2)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)   # Placement du cadre

    # Afficher la condition actuelle au démarrage
    display_condition_screen(main_frame)

    root.mainloop()       # Boucle principale de l'interface

#----------------------------------------------------------------------------------------


# 2.AFFICHAGE DES CONDITIONS ACTUELLES

# Ce bloc gère l'affichage des données sur les conditions actuelles comme la température et l'humidité.
def display_condition_screen(parent_frame):
    # Nettoyer le cadre
    for widget in parent_frame.winfo_children():
        widget.destroy()  # Supprime tous les widgets existants dans le cadre

    # Affichage de la condition actuelle
    tk.Label(parent_frame, text="Condition Actuelle", font=("Arial", 16, "bold"), bg="silver").pack(anchor="w", pady=5)

     # Dictionnaire des labels pour une organisation future
    labels = {
        "Température": tk.Label(parent_frame, text="Température : °C", font=("Arial", 12), bg="silver"),    # Ce widget 'Label' affiche la température actuelle comme texte statique.
                                                                                                # Il utilise une police Arial de taille 12, un fond silver, et est positionné avec un espacement vertical.
        "Humidité": tk.Label(parent_frame, text="Humidité : %", font=("Arial", 12),bg="silver"), #bg="silver").pack(anchor="w", padx=10, pady=5) est le positionnement
        "CO2": tk.Label(parent_frame, text="CO2 : ppm", font=("Arial", 12), bg="silver")
}
 # Appliquer.pack()à chaque label
    for label in labels.values():
        label.pack(anchor="w", padx=10, pady=5)   # anchor=W pour coté west, 

#----------------------------------------------------

    # Ajouter Lumière, Ventilation et Irrigation
    display_lighting_ventilation_irrigation(parent_frame)

       # Lancer la mise à jour des données dynamiques
    update_conditions(parent_frame, labels)
#----------------------------------------------------------------


#  2.1 LA FONCTION QUI VA ALLER CHERCHER LES DONNÉES
def update_conditions(parent_frame, labels):
    # Exemple de données simulées (remplacez par MongoDB plus tard)
    latest_data = {                         # latest_data = get_latest_environment_data() or {}  <<--- on remplace latest_date au moment daller chercher les donné dans mongo
        "Température": "28",                                                                              # le or {} est en faire une gestion d'erreur en cas de probleme dans la base de donner
        "Humidité": "55",
        "CO2": "420"
    }

    # Mettre à jour les valeurs dans les labels
    labels["Température"]["text"] = f"Température : {latest_data.get('Température', '--')}°C"
    labels["Humidité"]["text"] = f"Humidité : {latest_data.get('Humidité', '--')}%"
    labels["CO2"]["text"] = f"CO2 : {latest_data.get('CO2', '--')} ppm"

    # Replanifier la mise à jour après 1 seconde
    parent_frame.after(5000, update_conditions, parent_frame, labels)



#--------------------------------------------------------------------------------------------------------


# 3. GESTION DE LA LUMIERE, VENTILATION ET IRRIGATION

# Ce bloc ajoute des contrôles interactifs pour gérer la lumière, la ventilation et l'irrigation.
def display_lighting_ventilation_irrigation(parent_frame):
    # Ajouter Lumière, Ventilation et Irrigation
    bottom_frame = tk.Frame(parent_frame, bg="BLACK", relief=tk.GROOVE, borderwidth=2)
    bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)    # fill=tk.BOTH permet au cadre de s'étendre horizontalement et verticalement
                                                                       # expand=True permet d'utiliser tout l'espace disponible.
                                                                        # fill=tk.BOTH permet au cadre de s'étendre horizontalement et verticalement.
    # Fonction pour activer/désactiver une fonction spécifique
         # system : indique le système ciblé (Lumière, Ventilation, Irrigation).
         # status_var : variable tkinter (StringVar) pour l'état actuel (On/Off).
         # timer_entry : champ de saisie pour la minuterie
    def toggle_action(system, status_var, timer_entry=None):                     
        current_status = status_var.get()                               # Récupère la valeur actuelle de l'état (On ou Off).
        new_status = "On" if current_status == "Off" else "Off"         # Bascule l'état entre "On" et "Off" en fonction de la valeur actuelle.
        status_var.set(new_status)                                       # Met à jour l'état dans la variable tkinter (cela modifie également l'affichage).

        # Récupérer la valeur de la minuterie si disponible
        timer_value = timer_entry.get() if timer_entry else None        # Si timer_entry est défini, récupère la valeur saisie, sinon utilise None.
        try:
            timer_value = int(timer_value) if timer_value else 0          # Convertit la valeur de la minuterie en entier (int), ou utilise 0 si le champ est vide.
        except ValueError:
            timer_value = 0                                        # Si la conversion échoue (par exemple, si l'utilisateur entre du texte non valide), timer_value est défini à 0.

                # Appeler les fonctions de ton collègue en fonction du système
        if system == "Irrigation":
            print(f"Appel à la fonction de gestion d'irrigation d'Alex avec statut {new_status} et minuterie {timer_value}.")
            # Exemple : appel fictif à la fonction de ton collègue
            # activate_irrigation(new_status, timer_value)
        elif system == "Lumière":
            print(f"Appel à la fonction de gestion de lumière d'Alex avec statut {new_status} et minuterie {timer_value}.")
            # activate_lighting(new_status, timer_value)
        elif system == "Ventilation":
            print(f"Appel à la fonction de gestion de ventilation d'Alex avec statut {new_status} et minuterie {timer_value}.")
            # activate_ventilation(new_status, timer_value)


    # Lumière                                                                                                  # Crée une étiquette pour le système de lumière, placée à la première ligne (row=0) et première colonne (column=0).                         
    tk.Label(bottom_frame, text="Lumière :", font=("Arial", 12), bg="SILVER").grid(row=0, column=0, sticky="e")         # sticky="e" aligne le texte à droite.                               
    light_status = tk.StringVar(value="Off")                                                                                # Initialise une variable tkinter de type StringVar avec la valeur "Off" pour suivre l'état de la lumière.                                                                                                                                                             
    tk.Label(bottom_frame, textvariable=light_status, font=("Arial", 12), bg="SILVER", fg="green").grid(row=0, column=1, sticky="w")       # Affiche l'état actuel de la lumière (On/Off) à partir de light_status.                                                                                                                                     
    ttk.Button(bottom_frame, text="On/Off", command=lambda: toggle_action("Lumière", light_status)).grid(row=0, column=2, padx=10)            # command=lambda: toggle_action(...) appelle la fonction toggle_action avec les arguments spécifiés.
    ttk.Label(bottom_frame, text="Timer (min) :").grid(row=0, column=3, padx=5)                                                          # Crée une étiquette pour indiquer que l'utilisateur peut définir une minuterie.        
    light_timer = ttk.Entry(bottom_frame, width=5)                          # Création d'un champ de saisie (Entry) pour permettre à l'utilisateur d'entrer une valeur de minuterie pour la lumière.
    light_timer.grid(row=0, column=4)                                                      # 'width=5' limite la largeur du champ pour accepter des valeurs courtes comme des minutes.
# Positionnement du champ de saisie dans le tableau d'interface (grid)
# 'row=0' place ce champ sur la première ligne, et 'column=4' dans la cinquième colonne (en commençant à 0).

    # Ventilation
    tk.Label(bottom_frame, text="Ventilation :", font=("Arial", 12), bg="SILVER").grid(row=1, column=0, sticky="e")
    fan_status = tk.StringVar(value="Off")
    tk.Label(bottom_frame, textvariable=fan_status, font=("Arial", 12), bg="SILVER", fg="green").grid(row=1, column=1, sticky="w")
    ttk.Button(bottom_frame, text="On/Off", command=lambda: toggle_action("Ventilation", fan_status)).grid(row=1, column=2, padx=10)
    ttk.Label(bottom_frame, text="Timer (min) :").grid(row=1, column=3, padx=5)
    fan_timer = ttk.Entry(bottom_frame, width=5)
    fan_timer.grid(row=1, column=4)

    # Irrigation
    tk.Label(bottom_frame, text="Irrigation :", font=("Arial", 12), bg="SILVER").grid(row=2, column=0, sticky="e")
    irrigation_status = tk.StringVar(value="Off")
    tk.Label(bottom_frame, textvariable=irrigation_status, font=("Arial", 12), bg="SILVER", fg="green").grid(row=2, column=1, sticky="w")
    ttk.Button(bottom_frame, text="On/Off", command=lambda: toggle_action("Irrigation", irrigation_status)).grid(row=2, column=2, padx=10)
    ttk.Label(bottom_frame, text="Timer (min) :").grid(row=2, column=3, padx=5)
    irrigation_timer = ttk.Entry(bottom_frame, width=5)
    irrigation_timer.grid(row=2, column=4)




# 4  Résumé : Affichage du menu des tendances
# Ce bloc présente les moyennes des paramètres et un graphique fictif des tendances.
def display_trend_menu(parent_frame):
    # Nettoyer le cadre
    for widget in parent_frame.winfo_children():
        widget.destroy()   # Supprime tous les widgets existants

    # Cadre supérieur pour les moyennes et le graphique
    trend_frame = tk.Frame(parent_frame, bg="lightyellow", relief=tk.GROOVE, borderwidth=2)  # 'trend_frame' est un cadre avec un fond jaune clair et une bordure de style 'GROOVE'
                                                                                                # Il est destiné à organiser les widgets liés aux tendances.
    trend_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)                             

    # Section gauche : Moyennes pour la journée précédente
    left_frame = tk.Frame(trend_frame, bg="white", width=400)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(left_frame, text="Tendance : Moyennes de la journée précédente", font=("Arial", 14), bg="white").pack(pady=5)
    tk.Label(left_frame, text="Date : 2023-12-23", font=("Arial", 12), bg="white").pack(pady=5)
    tk.Label(left_frame, text="Température : 22°C", font=("Arial", 12), bg="white").pack(pady=5)
    tk.Label(left_frame, text="Humidité : 58%", font=("Arial", 12), bg="white").pack(pady=5)
    tk.Label(left_frame, text="CO2 : 390 ppm", font=("Arial", 12), bg="white").pack(pady=5)

    # Section droite : Graphique
    right_frame = tk.Frame(trend_frame, bg="white", width=600)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(right_frame, text="Graphique : Évolution des températures", font=("Arial", 14), bg="white").pack(pady=5)
    canvas = tk.Canvas(right_frame, width=500, height=300, bg="white")
    canvas.pack()
    canvas.create_line(50, 250, 450, 250, fill="black", width=2)  # Cette ligne crée un axe horizontal noir pour le graphique avec des coordonnées spécifiques (50, 250) à (450, 250) et une largeur de 2 pixels.
    canvas.create_line(50, 250, 50, 50, fill="black", width=2)  # Axe vertical (température)
    canvas.create_text(50, 260, text="0h", anchor="n", font=("Arial", 10))
    canvas.create_text(450, 260, text="24h", anchor="n", font=("Arial", 10))
    canvas.create_text(30, 50, text="Temp", anchor="e", font=("Arial", 10))
    canvas.create_line(50, 200, 100, 150, fill="red", width=2)  # Exemple de courbe

    # Section pour sélectionner une date
    date_frame = tk.Frame(parent_frame, bg="white", relief=tk.GROOVE, borderwidth=2)
    date_frame.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(date_frame, text="Sélectionner une date pour les moyennes :", font=("Arial", 14), bg="white").grid(row=0, column=0, columnspan=3, pady=10)
    
    ttk.Label(date_frame, text="Jour :").grid(row=1, column=0, padx=5)
    ttk.Combobox(date_frame, values=[str(i) for i in range(1, 32)]).grid(row=1, column=1, padx=5)
    ttk.Label(date_frame, text="Mois :").grid(row=1, column=2, padx=5)
    ttk.Combobox(date_frame, values=["Janvier", "Février", "Mars"]).grid(row=1, column=3, padx=5)
    ttk.Label(date_frame, text="Année :").grid(row=1, column=4, padx=5)
    ttk.Combobox(date_frame, values=["2022", "2023", "2024"]).grid(row=1, column=5, padx=5)

    tk.Button(date_frame, text="Afficher", command=lambda: messagebox.showinfo("Date", "Moyennes chargées pour la date sélectionnée.")).grid(row=1, column=6, padx=10)

    # Section pour conditions optimales et téléchargement
    bottom_frame = tk.Frame(parent_frame, bg="white", relief=tk.GROOVE, borderwidth=2)
    bottom_frame.pack(fill=tk.X, padx=10, pady=10)

    tk.Label(bottom_frame, text="Conditions Optimales :", font=("Arial", 14), bg="white").pack(pady=5)
    tk.Label(bottom_frame, text="Température : 20-25°C", font=("Arial", 12), bg="white").pack(pady=2)
    tk.Label(bottom_frame, text="Humidité : 50-70%", font=("Arial", 12), bg="white").pack(pady=2)
    tk.Label(bottom_frame, text="CO2 : 350-450 ppm", font=("Arial", 12), bg="white").pack(pady=2)

    tk.Button(bottom_frame, text="Télécharger les 5 dernières moyennes", command=download_csv).pack(pady=10)


# Résumé : Télécharger un fichier CSV
# Ce bloc permet à l'utilisateur de sauvegarder un fichier CSV contenant des données fictives.
def download_csv():
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")]) # 'filepath' utilise une boîte de dialogue pour demander à l'utilisateur de choisir où sauvegarder un fichier CSV.
                                                                                                         # L'extension par défaut est '.csv'.
    if filepath:
        with open(filepath, "w") as f:
            f.write("Exemple de moyennes, données fictives.\n")
        messagebox.showinfo("Téléchargement", "Fichier CSV téléchargé avec succès !")

# Résumé : Affichage des alertes
# Ce bloc affiche une boîte de dialogue indiquant qu'il n'y a pas d'alertes.
def show_alerts(root, parent_frame):
    messagebox.showinfo("Alertes", "Aucune alerte pour le moment.")     # Ce 'messagebox' affiche une boîte de dialogue avec un message informant qu'aucune alerte n'est actuellement disponible.


# Lancement de l'application principale
if __name__ == "__main__":
    main_interface()
