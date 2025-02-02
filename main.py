import tkinter as tk
from condition_et_gestion import condition_actuelles
from tendance import afficher_menu_tendances
from gestion_alertes import creer_fenetre_alertes
from chargement import get_alerts, load_environment, load_optimal_thresholds
from ajouter_donne import ajoute_donne
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
    load_environment("environment.json")
    # Dans main_interface(), après le chargement de environment_data
    optimal_thresholds = load_optimal_thresholds("optimal_threshold.json")
    print("Seuils optimaux chargés :", optimal_thresholds)

    # Fonction pour mettre à jour le label des alertes
    def update_alerts_label():
        nb_alertes = get_alerts("alertes.json")
        menu_bar.entryconfig(3, label=f"Afficher les alertes ({nb_alertes})")
        root.after(1000, update_alerts_label)
    
    # Démarrer la mise à jour périodique des alertes
    update_alerts_label()
    
    # Afficher les conditions actuelles par défaut
    condition_actuelles(main_frame)
    
    root.mainloop()

if __name__ == "__main__":
    main_interface()



