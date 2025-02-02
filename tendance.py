# Importation des bibliothèques nécessaires
import tkinter as tk  # Pour créer l'interface graphique
from tkinter import ttk, messagebox  # Éléments modernes et boîtes de dialogue
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Intégration des graphiques
import matplotlib.pyplot as plt  # Création de graphiques
from chargement import open_env_data  # Notre propre fonction pour lire les données


# --------------------------- PARTIE 1 : INTERFACE PRINCIPALE ---------------------------

def afficher_menu_tendances(parent_frame):
    # On nettoie l'écran précédent en supprimant tous les éléments
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Création du cadre principal (la "feuille" où tout sera dessiné)
    frame_principale = tk.Frame(parent_frame, bg="#CDCDB4", relief=tk.GROOVE, borderwidth=2)
    frame_principale.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Titre principal de la page
    tk.Label(frame_principale, text="Tendances Moyennes en Date du :", font=("Arial", 16, "bold"), bg="#CDCDB4").pack(pady=10)
    
    # Création d'une zone pour regrouper jour/mois/année et valeurs actuelles
    top_frame = tk.Frame(frame_principale, bg="#8B8B7A")
    top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

    # 1.2 SECTION GAUCHE : COMBOBOX, SELECTEUR DATE  ---------------------------
    frame_gauche = tk.Frame(top_frame, bg="#8B8B7A")
    frame_gauche.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    # Étiquettes pour  les menus déroulants
    tk.Label(frame_gauche, text="Jour", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=0, padx=5, pady=2)
    tk.Label(frame_gauche, text="Mois", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=1, padx=5, pady=2)
    tk.Label(frame_gauche, text="Année", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=2, padx=5, pady=2)
    
    # Création des menus déroulants avec des valeurs prédéfinies
    # zfill(2) ajoute un zéro devant les chiffres <10 (ex: '1' devient '01')
    jour_combo = ttk.Combobox(frame_gauche, values=[str(i).zfill(2) for i in range(1, 32)], width=4, state="readonly")
    mois_combo = ttk.Combobox(frame_gauche, values=[str(i).zfill(2) for i in range(1, 13)], width=6, state="readonly")
    annee_combo = ttk.Combobox(frame_gauche, values=[str(i) for i in range(2020, 2026)], width=6, state="readonly")

    # Placement des menus déroulants dans la grille
    jour_combo.grid(row=1, column=0, padx=5, pady=2)
    mois_combo.grid(row=1, column=1, padx=5, pady=2)
    annee_combo.grid(row=1, column=2, padx=5, pady=2)

    # 1.2 SECTION droite: afficher les parametre avec la derniere valeur de la journée ---------------------------
    frame_de_droite = tk.Frame(top_frame, bg="#8B8B7A", relief=tk.GROOVE, borderwidth=2)
    frame_de_droite.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Dictionnaire qui contient les étiquettes des valeurs 
    nom_des_parametre = {
        "date": tk.Label(frame_de_droite, text="Date : ", font=("Arial", 12), bg="#8B8B7A"),
        "temp": tk.Label(frame_de_droite, text="Température : -- °C", font=("Arial", 12), bg="#8B8B7A"),
        "humidity": tk.Label(frame_de_droite, text="Humidité : -- %", font=("Arial", 12), bg="#8B8B7A"),
        "co2": tk.Label(frame_de_droite, text="CO2 : -- ppm", font=("Arial", 12), bg="#8B8B7A")
    }

    # Placement des étiquettes dans la partie de droite
    nom_des_parametre["date"].grid(row=0, column=0, sticky="w", padx=10, pady=5)
    nom_des_parametre["temp"].grid(row=1, column=0, sticky="w", padx=10, pady=5)
    nom_des_parametre["humidity"].grid(row=2, column=0, sticky="w", padx=10, pady=5)
    nom_des_parametre["co2"].grid(row=3, column=0, sticky="w", padx=10, pady=5)

    def update_current_values(data):
        
        if data:  # Si on a des données...
            latest = data[-1]  # On prend la dernière mesure de la journée
            # On met à jour les textes comme on changerait une étiquette
            nom_des_parametre["temp"].config(text=f"Température : {latest['Température']}°C")
            nom_des_parametre["humidity"].config(text=f"Humidité : {latest['Humidité']}%")
            nom_des_parametre["co2"].config(text=f"CO2 : {latest['CO2']} ppm")
            nom_des_parametre["date"].config(text=f"Date : {latest['Date']}")

    # =============== Partie 2 Creation Bouton "Afficher" SECTION GAUCHE en dessous des Combobox SECTION GAUCHE
    def on_button_click():
        # Récupération des valeurs sélectionnées
        day = jour_combo.get()
        month = mois_combo.get()
        year = annee_combo.get()

        # Vérification que tous les champs sont remplis
        if not day or not month or not year:
            messagebox.showwarning("Erreur", "Veuillez sélectionner une date complète.")
            return

        date_choisi = f"{year}-{month}-{day}"  # Création de la date formatée
        
        # Chargement des données depuis le fichier JSON
        data = open_env_data("environment.json")
        filtered_data = []  # Liste vide qu'on va remplir
        
        # Filtrage : on garde seulement les données de la date choisie
        for entry in data:
            entry_date = entry["Date"].split()[0]  # On prend que la partie date (sans l'heure) ********
            if entry_date == date_choisi:                                                     #  ********
                filtered_data.append(entry)  # Ajout à la liste si ça correspond              #***********
        
        # Tri des données par heure (comme ranger des livres dans l'ordre)
        filtered_data.sort(key=lambda x: x["Date"].split()[1])                      #************************

        # Si aucune donnée n'a été trouvée...
        if not filtered_data:
            messagebox.showwarning("Erreur", f"Aucune donnée disponible pour la date {date_choisi}.")
            return

        # Mise à jour de l'interface et du graphique
        update_current_values(filtered_data)
        tracer_graphique(parameter_combox.get(), frame_du_bas, filtered_data)

    # Création du bouton Afficher
    ttk.Button(frame_gauche, text="Afficher", command=on_button_click).grid(row=2, column=0, columnspan=3, pady=10)

    #  PARAMÈTRES : Choix de la courbe à afficher 
    frame_parametre = tk.Frame(frame_principale, bg="lightyellow")
    frame_parametre.pack(pady=5)
    
    # Ici le combobox qui permet de selection  ["Température", "Humidité", "CO2"] 
    tk.Label(frame_parametre, text="Paramètre :", font=("Arial", 12), bg="lightyellow").pack(side=tk.LEFT, padx=5)
    parameter_combox = ttk.Combobox(frame_parametre, values=["Température", "Humidité", "CO2"], state="readonly")
    parameter_combox.set("Température")  # Valeur par défaut
    parameter_combox.pack(side=tk.LEFT, padx=5)

    # ------  Zone du GRAPHIQUE en bas ------
    frame_du_bas = tk.Frame(frame_principale, bg="white", height=400)
    frame_du_bas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def on_parameter_change(_):
        """Quand on change le paramètre, on met à jour le graphique"""
        if "date" in nom_des_parametre:
            # Récupération de la date actuellement affichée
            date_text = nom_des_parametre["date"].cget("text")
            if ":" in date_text and len(date_text.split(": ")) > 1:
                date_complete = date_text.split(": ")[1]
                selected_date = date_complete.split()[0]  # On extrait la date
                
                # Rechargement et filtrage des données (comme précédemment)
                data = open_env_data("environment.json")
                filtered_data = []
                
                for entry in data:
                    entry_date = entry["Date"].split()[0]
                    if entry_date == selected_date:
                        filtered_data.append(entry)
                
                filtered_data.sort(key=lambda x: x["Date"].split()[1])

                if filtered_data:
                    tracer_graphique(parameter_combox.get(), frame_du_bas, filtered_data)

    # On lie le changement de paramètre à la fonction de mise à jour
    parameter_combox.bind("<<ComboboxSelected>>", on_parameter_change)


# ================================ PARTIE 3 : TRACER LE GRAPHIQUE ===========================================
def tracer_graphique(parameter, frame, data):
    """Fonction qui dessine le graphique dans la zone prévue"""
    # On nettoie l'ancien graphique
    for widget in frame.winfo_children():
        widget.destroy()

    # Extraction des heures et valeurs (ex: ["12:00", "13:00"], [25, 26])
    heures = [entry["Date"].split()[1] for entry in data]
    valeurs = [entry[parameter] for entry in data]

    # Création de la figure (la "toile" du graphique)
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Dessin de la courbe avec des options de style
    ax.plot(heures, valeurs, 
            marker='o',         # Forme des points
            color='#2196F3',    # Couleur bleue
            linewidth=2,        # Épaisseur de la ligne
            markersize=8,       # Taille des points
            markerfacecolor='white',  # Intérieur des points
            markeredgewidth=2)  # Bordure des points
    
    # Personnalisation du titre
    ax.set_title(f"Évolution de {parameter} le {data[0]['Date'].split()[0]}", 
                 fontsize=14, pad=20, fontweight='bold')
    
    # Ajout d'une grille en arrière-plan
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Étiquettes des axes
    ax.set_xlabel("Heures", fontsize=12, labelpad=10)
    ax.set_ylabel(f"{parameter} {'(°C)' if parameter == 'Température' else '(%)' if parameter == 'Humidité' else '(ppm)'}", 
                  fontsize=12, labelpad=10)
    
    # Rotation des heures pour mieux les lire
    plt.xticks(rotation=45)
    
    # Ajustement de l'espacement
    plt.tight_layout()

    # Intégration du graphique dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# =================== Lancement de l'application si on exécute ce fichier directement sans le main =======================
if __name__ == "__main__":
    root = tk.Tk()  # Création de la fenêtre principale
    root.title("Gestion de la Serre Intelligente")
    root.geometry("1200x800")  # Taille initiale
    afficher_menu_tendances(root)  # On affiche notre interface
    root.mainloop()  # Démarrage de la boucle principale (comme un moteur qui tourne)