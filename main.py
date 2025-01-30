import tkinter as tk  # Module principal de Tkinter pour créer des interfaces graphiques
from tkinter import ttk  # Module Tkinter pour des widgets thématiques
from condition_et_gestion import condition_actuelles  # Fonction pour afficher les conditions actuelles
from tendance import afficher_menu_tendances  
from gestion_alertes import creer_fenetre_alertes  # Appel des fonctions de gestion des alertes
from chargement import get_alerts
#from ajouter_donne import ajoute_donne


# --------------------------- INTERFACE PRINCIPALE ---------------------------
def main_interface():
    root = tk.Tk()
    root.title("Serre Intelligente - SMAG")  # Titre de la fenêtre
    root.geometry("1200x800")  # Taille de la fenêtre (largeur x hauteur)
    root.config(bg="#1E1E1E")  # Couleur de fond de la fenêtre principale

     # Création du cadre principal pour afficher le contenu dynamique
    main_frame = tk.Frame(root, bg="#303030", relief=tk.SUNKEN, borderwidth=2)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    #json_f = chargement.get_alerts("alerts.json", None)  # Nom du fichier JSON contenant les alertes
    a = get_alerts("alerts.json")  # Récupération du nombre d'alertes
    
    # Création de la barre de menu avec différentes options
    menu_bar = tk.Menu(root)
    menu_bar.add_command(label="Condition Actuelle", command=lambda: condition_actuelles(main_frame))
    menu_bar.add_command(label="Tendance", command=lambda: afficher_menu_tendances(main_frame))
    menu_bar.add_command(label=f"Afficher les alertes ({a})", command=creer_fenetre_alertes)  # Affiche le nombre d'alertes
    #menu_bar.add_command(label="Ajouter les données des capteurs", command=lambda: ajoute_donne(main_frame))
    
    root.config(menu=menu_bar)  # la commande menu_bar = tk.Menu(root) a besoin de cette config pour etre afficher
    
    condition_actuelles(main_frame)  # Affichage par défaut des conditions actuelles
    
    root.mainloop()  # Démarrage de la boucle principale de l'interface graphique

# --------------------------- POINT D'ENTRÉE DU PROGRAMME ---------------------------
if __name__ == "__main__":
    main_interface()  # Lancement de l'interface principale



