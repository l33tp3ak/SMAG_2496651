import tkinter as tk

import chargement
from condition_et_gestion import condition_actuelles
from tendance import afficher_menu_tendances
from gestion_alertes import creer_fenetre_alertes, nombre_alertes
from ajouter_donne import ajoute_donne
import add_data
from afficher_dernier_donner import afficher_dernieres_donnees

# ===============Partie 1 : on cree le menu interactif avec les add.command =========================
def main_interface():
    root = tk.Tk()
    root.title("Serre Intelligente - SMAG")
    root.geometry("1200x800")
    root.config(bg="#1E1E1E")

    main_frame = tk.Frame(root, bg="#303030", relief=tk.SUNKEN, borderwidth=2)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    

    
    # Créer un menu qui peut être mis à jour
    menu_bar = tk.Menu(root)
    
    # Ajouter les éléments du menu sans le compteur d'alertes initial
    menu_bar.add_command(label="Condition Actuelle", command=lambda: condition_actuelles(main_frame))
    menu_bar.add_command(label="Tendance", command=lambda: afficher_menu_tendances(main_frame))
    menu_bar.add_command(label="Afficher les alertes", command=creer_fenetre_alertes)  # Sans le compteur initial
    menu_bar.add_command(label="Ajouter les données des capteurs", command=lambda: ajoute_donne(main_frame))
    menu_bar.add_command(label="Dernières données", command=afficher_dernieres_donnees)
    root.config(menu=menu_bar)
    

    # =============  Partie 2 on charge tout les fichier json  ===================
    chargement.open_data("environment.json")
    # Dans main_interface(), après le chargement de environment_data
    optimal_thresholds = chargement.open_data("optimal_threshold.json")
    print("Seuils optimaux chargés :", optimal_thresholds)

    # Fonction pour mettre à jour le label des alertes
    def update_alerts_label():
        nb_alertes = nombre_alertes()
        menu_bar.entryconfig(3, label=f"Afficher les alertes ({nb_alertes})")
        root.after(6000, update_alerts_label)

    def update_sensors():
        add_data.auto_sensor_data()
        # Mise a jour toute les 10 minutes
        root.after(600000, update_sensors)

    def export_full_data_to_csv():
        alertes = chargement.open_data("alertes.json")
        environment = chargement.open_data("environment.json")
        chargement.export_data_to_csv(alertes, "alertes.csv")
        chargement.export_data_to_csv(environment, "environment.csv")
        # Ceci ferme TOUTES les fenêtres, car nous interceptons le protocol de sorti ET il ferme également l'interpréteur.
        # Ainsi, TOUS les processus reliés au programme sont fermés en même temps.
        root.destroy()
        exit()

    #def update_environment():
    # Démarrer la mise à jour périodique des alertes et des capteurs
    update_alerts_label()
    update_sensors()
    
    # Afficher les conditions actuelles par défaut
    condition_actuelles(main_frame)
    # Lorsque l'utilisateur ferme la fenêtre, on appelle la fonction export_full_data_to_csv()
    root.protocol("WM_DELETE_WINDOW", export_full_data_to_csv)
    root.mainloop()

if __name__ == "__main__":
    main_interface()



