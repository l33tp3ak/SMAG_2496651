from chargement import open_env_data, export_full_data_to_csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

def afficher_dernieres_donnees():
    fenetre = tk.Toplevel()
    fenetre.title("Dernières mesures")
    fenetre.geometry("800x600")
    fenetre.configure(bg="#303030")

    data = open_env_data("environment.json")
    if not data:
        tk.Label(fenetre, text="Aucune donnée disponible", bg="#303030", fg="white").pack(pady=20)
        return

    try:
        data_triee = sorted(data, key=lambda x: datetime.strptime(x["Date"], "%Y-%m-%d %H:%M"), reverse=True)[:5]
    except Exception as e:
        tk.Label(fenetre, text=f"Erreur: {str(e)}", bg="#303030", fg="white").pack()
        return

    main_frame = tk.Frame(fenetre, bg="#303030")
    main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Titre
    tk.Label(main_frame, text="5 Dernières Mesures", font=("Arial", 14, "bold"), bg="#CDCDB4", fg="#303030").pack(fill=tk.X, pady=10)

    for i, mesure in enumerate(data_triee, 1):
        frame_mesure = tk.Frame(main_frame, bg="#303030", relief=tk.GROOVE, bd=2)
        frame_mesure.pack(fill=tk.X, pady=5, padx=10)
        
        date_obj = datetime.strptime(mesure["Date"], "%Y-%m-%d %H:%M")
        date_formatee = date_obj.strftime("%d/%m/%Y %H:%M")
        
        tk.Label(frame_mesure, text=f"Mesure #{i} - {date_formatee}", bg="#303030", fg="white", font=("Arial", 11)).grid(row=0, column=0, columnspan=4, sticky=tk.W)
        tk.Label(frame_mesure, text=f"🌡 {mesure['Température']}°C", bg="#303030", fg="white").grid(row=1, column=0, padx=10)
        tk.Label(frame_mesure, text=f"💧 {mesure['Humidité']}%", bg="#303030", fg="white").grid(row=1, column=1, padx=10)
        tk.Label(frame_mesure, text=f"💡 {mesure['Lumière']} lux", bg="#303030", fg="white").grid(row=1, column=2, padx=10)
        tk.Label(frame_mesure, text=f"🏭 {mesure['CO2']} ppm", bg="#303030", fg="white").grid(row=1, column=3, padx=10)

    # Boutons
    btn_frame = tk.Frame(main_frame, bg="#303030")
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="📤 Exporter en CSV", bg="#CDCDB4", fg="#303030",
             command=handle_csv_export).pack(side=tk.LEFT, padx=10)
    
    tk.Button(main_frame, text="Fermer", command=fenetre.destroy, bg="#CDCDB4", fg="#303030").pack(pady=20)

def handle_csv_export():
    """Gère l'export CSV avec feedback utilisateur"""
    try:
        filename = export_full_data_to_csv()
        messagebox.showinfo("Succès", f"Données exportées avec succès dans :\n{filename}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'export :\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    afficher_dernieres_donnees()
    root.mainloop()