from chargement import open_data, export_data_to_csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def afficher_dernieres_donnees():
    fenetre = tk.Toplevel()
    fenetre.title("Dernières mesures")
    fenetre.geometry("800x600")
    fenetre.configure(bg="#303030")

    data = open_data("environment.json")
    if not data:
        tk.Label(fenetre, text="Aucune donnée disponible", bg="#303030", fg="white").pack(pady=20)
        return

    try:
        data_triee = sorted(data.keys(), key=lambda x: datetime.strptime(x, "%d %B %Y %I:%M%p"), reverse=True)[:5]
    except Exception as e:
        tk.Label(fenetre, text=f"Erreur: {str(e)}", bg="#303030", fg="white").pack()
        return

    main_frame = tk.Frame(fenetre, bg="#303030")
    main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Titre
    tk.Label(main_frame, text="5 Dernières Mesures", font=("Arial", 14, "bold"), bg="#CDCDB4", fg="#303030").pack(fill=tk.X, pady=10)
    export_dict = {}
    seuil = open_data("optimal_threshold.json")
    absolute_zero = -273.15

    # Compense pour les donnees inexistante en les remplacant par 0
    for i, date in enumerate(data_triee, 0):
        for parametre in seuil:  # On prend que la partie date ********
            print(parametre)
            print(data_triee[i])
            if data[date].get(parametre) is None:
                if parametre == "Température":
                    data[date][parametre] = absolute_zero
                else:
                    data[date][parametre] = 0


    for i, date in enumerate(data_triee, 0):
        export_dict[date] = data[date]
        print(date)
        frame_mesure = tk.Frame(main_frame, bg="#303030", relief=tk.GROOVE, bd=2)
        frame_mesure.pack(fill=tk.X, pady=5, padx=10)
        
        tk.Label(frame_mesure, text=f"Mesure #{i} - {date}", bg="#303030", fg="white", font=("Arial", 11)).grid(row=0, column=0, columnspan=4, sticky=tk.W)
        tk.Label(frame_mesure, text=f"🌡 {data[date]['Température']}°C", bg="#303030", fg="white").grid(row=1, column=0, padx=10)
        tk.Label(frame_mesure, text=f"💧 {data[date]['Humidité']}%", bg="#303030", fg="white").grid(row=1, column=1, padx=10)
        tk.Label(frame_mesure, text=f"💡 {data[date]['Lumière']} lux", bg="#303030", fg="white").grid(row=1, column=2, padx=10)
        tk.Label(frame_mesure, text=f"🏭 {data[date]['CO2']} ppm", bg="#303030", fg="white").grid(row=1, column=3, padx=10)

    # Boutons
    btn_frame = tk.Frame(main_frame, bg="#303030")
    btn_frame.pack(pady=20)
    # Une fonction anonyme "lambda" est nécessaire car sinon la fonction à laquelle on passe un argument est appellée immédiatement.
    # Ceci crée un bouton qui appel notre command d'export vers CSV et lui transmet notre dictionnaire contenant ce que l'on désire export, ici les 5 dernière données.
    tk.Button(btn_frame, text="📤 Exporter en CSV", bg="#CDCDB4", fg="#303030", command=lambda: handle_csv_export(export_dict)).pack(side=tk.LEFT, padx=10)
    
    tk.Button(main_frame, text="Fermer", command=fenetre.destroy, bg="#CDCDB4", fg="#303030").pack(pady=20)

def handle_csv_export(donnee_triee):
    """Gère l'export CSV avec feedback utilisateur"""
    filename = export_data_to_csv(donnee_triee)
    messagebox.showinfo("Succès", f"Données exportées avec succès dans :\n{filename}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    afficher_dernieres_donnees()
    root.mainloop()