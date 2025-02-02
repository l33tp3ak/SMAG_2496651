# gestion_alertes.py

import tkinter as tk
from tkinter import ttk
from chargement import open_env_data
from datetime import datetime

def creer_fenetre_alertes():
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
    alertes = open_env_data("alertes.json")
    groupes = {}
    for alerte in alertes:
        parametre = alerte["paramètre"]
        groupes.setdefault(parametre, []).append(alerte)  # Regroupement par paramètre

    # Style pour les en-têtes de section
    style = ttk.Style()
    style.configure("Groupe.TLabel", font=('Arial', 12, 'bold'), background="#CDCDB4", foreground="#303030")

    # Affichage des alertes groupées et triées
    for parametre in sorted(groupes.keys()):
        # En-tête de section avec couleur beige
        ttk.Label(scrollable_frame, text=f"Alertes {parametre.capitalize()} :", style="Groupe.TLabel").pack(fill="x", padx=10, pady=(15, 5))
        
        # Tri des alertes par date (récent -> ancien)
        alertes_triees = sorted(groupes[parametre], key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M"), reverse=True)
        
        # Affichage de chaque alerte
        for alerte in alertes_triees:
            date_formatee = datetime.strptime(alerte["timestamp"], "%Y-%m-%d %H:%M").strftime("%d/%m/%Y à %H:%M")
            texte = f"• {alerte['valeur']}{unite(parametre)} - {alerte['message']} (le {date_formatee})"
            # Label avec fond gris et texte clair
            ttk.Label(scrollable_frame, text=texte, background="#303030", foreground="white", padding=(20, 5)).pack(fill="x", padx=20)

    # Mise à jour finale de l'affichage
    scrollable_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    return fenetre

def unite(parametre):
    # Dictionnaire des unités de mesure
    return {"Température": "°C", "Humidité": "%", "CO2": "ppm", "Lumière": "lux"}.get(parametre, "")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    creer_fenetre_alertes()
    root.mainloop()




    





