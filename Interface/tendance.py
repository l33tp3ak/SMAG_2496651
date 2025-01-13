import tkinter as tk  
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import backend_

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
    # Conteneur gauche (sélecteur de date)
    frame_gauche = tk.Frame(top_frame, bg="#8B8B7A")
    frame_gauche.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    # Labels pour les sélecteurs
    tk.Label(frame_gauche, text="Jour", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=0, padx=5, pady=2)
    tk.Label(frame_gauche, text="Mois", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=1, padx=5, pady=2)
    tk.Label(frame_gauche, text="Année", font=("Arial", 10), bg="#8B8B7A").grid(row=0, column=2, padx=5, pady=2)
    
    # 1.3 SECTION MILIEU : VALEURS ENVIRONNEMENTALES ---------------------------
    # Création du conteneur pour les valeurs environnementales
    frame_millieu = tk.Frame(top_frame, bg="#8B8B7A", relief=tk.GROOVE, borderwidth=2)
    frame_millieu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Création des labels parametre pour afficher la date,temperature,co2...
    nom_des_parametre = {
        "date": tk.Label(frame_millieu, text="Date : ", font=("Arial", 12), bg="#8B8B7A"),
        "temp": tk.Label(frame_millieu, text="Température :", font=("Arial", 12), bg="#8B8B7A"),
        "humidity": tk.Label(frame_millieu, text="Humidité : ", font=("Arial", 12), bg="#8B8B7A"),
        "co2": tk.Label(frame_millieu, text="CO2 :", font=("Arial", 12), bg="#8B8B7A")    }
    
    # Placement des labels des nom des param
    nom_des_parametre["date"].grid(row=0, column=0, sticky="w", padx=10, pady=5)
    nom_des_parametre["temp"].grid(row=1, column=0, sticky="w", padx=60, pady=5)
    nom_des_parametre["humidity"].grid(row=2, column=0, sticky="w", padx=60, pady=5)
    nom_des_parametre["co2"].grid(row=3, column=0, sticky="w", padx=60, pady=5)

    # 1.4 SECTION DROITE Conteneur droit (conditions optimales) APPEL LA FONCTION POUR LIBÉRER DE L'ESPACE -----------
    frame_droite = conditions_optimal(top_frame)
    frame_droite.pack(side=tk.RIGHT, padx=10)

    #1.5 Sélecteur de paramètre pour choisir le graphique aficher APELLE LA FONCTION qui choisie quelle graph afficher ( temperature,co2.humi)-----
    parameter_pour_graph, parameter_combox = selecteur_parametre_graph(frame_principale)
    parameter_pour_graph.pack(pady=5)

    # 1.6 frame du graphique en bas ------------------------
    frame_du_bas = tk.Frame(frame_principale, bg="white", height=400)
    frame_du_bas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

    #La fonction selecteur_date crée et retourne un tk.Frame qui contient des sélecteurs de date (jour, mois, année) sous forme de combobox, ainsi qu'un bouton pour valider la sélection
    date_selector = selecteur_date(frame_gauche, nom_des_parametre, parameter_combox, frame_du_bas)    #<¬¬¬¬
    date_selector.pack(pady=10)                                                                        #    -
                                                                                                       #    - 
                                                                                                       #    - 
# ---------------------------PARTIE 2 :  SECTION GAUCHE, SÉLECTEUR DE DATE --------------------------- #    - 
def selecteur_date(frame_gauche, nom_des_parametre, parameter_combox, frame_du_bas):                   # <----     

    # Combobox pour la sélection
    jour_combo = ttk.Combobox(frame_gauche, values=[str(i) for i in range(1, 32)], width=4, state="readonly")
    mois_combo = ttk.Combobox(frame_gauche, values=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"], width=6, state="readonly")
    annee_combo = ttk.Combobox(frame_gauche, values=[str(i) for i in range(2020, 2026)], width=6, state="readonly")

    jour_combo.grid(row=1, column=0, padx=5, pady=2)
    mois_combo.grid(row=1, column=1, padx=5, pady=2)
    annee_combo.grid(row=1, column=2, padx=5, pady=2)

    def on_parameter_selected(selected_parameter):
        selected_date = nom_des_parametre["date"].cget("text").split(": ")[1] if "date" in nom_des_parametre else None
        if selected_date:
            tracer_graphique(selected_parameter, frame_du_bas, selected_date)

    def on_button_click():
        day = jour_combo.get().zfill(2)
        month = mois_combo.get().zfill(2)
        year = annee_combo.get()
        if not (day and month and year):
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            return
        date_choisi = f"{year}-{month}-{day}"
        # Met à jour les valeurs moyennes via la fonction .update_moyenne dans le fichier backend_
        backend_.update_moyenne(date_choisi, nom_des_parametre)
        parametre_choisi = parameter_combox.get()
        tracer_graphique(parametre_choisi, frame_du_bas, date_choisi)

    ttk.Button(frame_gauche, text="Afficher", command=on_button_click).grid(row=2, column=0, columnspan=3, pady=10)
    
    # Ajout de la liaison pour le changement de paramètre
    parameter_combox.bind("<<ComboboxSelected>>", lambda event: on_parameter_selected(parameter_combox.get()))
    
    return frame_gauche

# --------------------------- PARTIE 3 SECTION DROITE, CONDITIONS OPTIMALES ---------------------------
def conditions_optimal(parent):
    """
    Crée le cadre des conditions optimales dans le conteneur de droite.
    """
    frame = tk.Frame(parent, bg="palegreen", relief=tk.GROOVE, borderwidth=2)
    tk.Label(frame, text="Conditions Optimales", font=("Arial", 14), bg="palegreen").pack(pady=5)
    tk.Label(frame, text="Température : 20-25°C", font=("Arial", 12), bg="palegreen").pack(pady=2)
    tk.Label(frame, text="Humidité : 50-70%", font=("Arial", 12), bg="palegreen").pack(pady=2)
    tk.Label(frame, text="CO2 : 350-450 ppm", font=("Arial", 12), bg="palegreen").pack(pady=2)
    return frame

# ---------------------------PARTIE 4 :  SECTION GRAPHIQUE ---------------------------
def selecteur_parametre_graph(parent):
    """
    Crée le sélecteur de paramètre pour le graphique.
    """
    frame = tk.Frame(parent, bg="lightyellow")
    tk.Label(frame, text="Paramètre :", font=("Arial", 12), bg="lightyellow").pack(side=tk.LEFT, padx=5)

    parameter_cb = ttk.Combobox(frame, values=["Température", "Humidité", "CO2"], state="readonly")
    parameter_cb.set("Température")
    parameter_cb.pack(side=tk.LEFT, padx=5)

    return frame, parameter_cb

def tracer_graphique(parameter, frame, date):
    """
    Trace le graphique des données environnementales.
    """
    detailed_data = backend_.get_detailed_trend_data(date)
    if not detailed_data:
        messagebox.showwarning("Erreur", f"Aucune donnée disponible pour la date {date}.")
        return

    hourly_data = detailed_data
    hours = list(hourly_data.keys())
    values = [hourly_data[hour][parameter] for hour in hours]

    for widget in frame.winfo_children():
        widget.destroy()

    ranges = {
        "Température": (15, 20, 25, 32),
        "Humidité": (30, 50, 70, 90),
        "CO2": (200, 350, 450, 1800),
    }

    critical_low, optimal_min, optimal_max, critical_high = ranges.get(parameter, (min(values), min(values), max(values), max(values)))

    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Zones de couleur
    ax.axhspan(critical_low, optimal_min, color="red", alpha=0.2)
    ax.axhspan(optimal_min, optimal_max, color="green", alpha=0.2)
    ax.axhspan(optimal_max, critical_high, color="red", alpha=0.2)
    ax.axhspan(optimal_max, critical_high, color="white", alpha=1)
    ax.axhspan(critical_low, optimal_min, color="white", alpha=1)

    ax.plot(hours, values, marker='o', color='blue', label=parameter)
    ax.set_title(f"Évolution de {parameter} - {date}", fontsize=14)
    ax.set_xlabel("Heures")
    ax.set_ylabel(parameter)
    ax.grid(True)
    ax.legend()

    margin = 2
    y_min = max(critical_low - margin, min(values) - margin)
    y_max = min(critical_high + margin, max(values) + margin)
    ax.set_ylim(y_min, y_max)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestion de la Serre Intelligente")
    root.geometry("800x600")
    afficher_menu_tendances(root)
    root.mainloop()