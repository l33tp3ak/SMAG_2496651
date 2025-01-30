# gestion_alertes.py

import tkinter as tk
from tkinter import ttk
from chargement import open_env_data, save_env_data

# --------------------------- PARTIE 1 : FONCTIONS POUR LA GESTION DES ALERTES ---------------------------

def creer_fenetre_alertes():
    """
    Crée une fenêtre pour afficher et gérer les alertes.
    """
    fenetre_alertes = tk.Toplevel()
    fenetre_alertes.title("Voir les alertes")
    fenetre_alertes.geometry("600x400")
    fenetre_alertes.configure(bg="#8B8B7A")

    frame_alertes = tk.Frame(fenetre_alertes, bg="#8B8B7A")
    frame_alertes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Menu local pour ajouter des alertes
    menu_local = tk.Menu(fenetre_alertes)
    fenetre_alertes.config(menu=menu_local)
    menu_local.add_command(label="Ajouter une alerte", command=lambda: ajouter_alerte(fenetre_alertes, frame_alertes))

    # Affichage initial des alertes
    rafraichir_alertes(frame_alertes)

#--------------  PARTIE 2 : MISE à jour dynamiquement de l'affichage
def rafraichir_alertes(frame_alertes):
    """
    Rafraîchit l'affichage des alertes dans la fenêtre.
    """
    for widget in frame_alertes.winfo_children():
        widget.destroy()  # Supprimer les widgets existants

    alertes = open_env_data("alerts.json")  # Charger les alertes depuis le fichier JSON

    if alertes:
        for alerte in alertes:
            texte_alerte = f"{alerte['Date']} - {alerte['Parametre']}: {alerte['Valeur']} ({alerte['Message']})"
            tk.Label(frame_alertes, text=texte_alerte, wraplength=550, bg="#CDCDB4", relief=tk.GROOVE, padx=5, pady=5).pack(fill=tk.X, pady=2)
    else:
        tk.Label(frame_alertes, text="Aucune alerte enregistrée.", bg="#CDCDB4", pady=20).pack()

# --------------------------- PARTIE 3 : AJOUT D'UNE ALERTE ---------------------------
def ajouter_alerte(fenetre_parent, frame_alertes):
    """Ouvre une nouvelle fenêtre pour ajouter une alerte"""
    fenetre_ajout = tk.Toplevel(fenetre_parent)
    fenetre_ajout.title("Ajouter une alerte")
    fenetre_ajout.geometry("400x500")
    fenetre_ajout.configure(bg="#8B8B7A")

    # Section Date
    ttk.Label(fenetre_ajout, text="Date (JJ/MM/AAAA):").pack(pady=5)
    cadre_date = tk.Frame(fenetre_ajout, bg="#8B8B7A")
    cadre_date.pack(pady=5)

    # Combobox pour le jour
    jours = [str(i).zfill(2) for i in range(1, 32)]
    jour_combo = ttk.Combobox(cadre_date, values=jours, width=4, state="readonly")
    jour_combo.grid(row=0, column=0, padx=2)

    # Combobox pour le mois
    mois_de_annee = ("Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre")
    mois_combo = ttk.Combobox(cadre_date, values=mois_de_annee, width=8, state="readonly")
    mois_combo.grid(row=0, column=1, padx=2)

    # Combobox pour l'année
    annees = [str(i) for i in range(2020, 2026)]
    annee_combo = ttk.Combobox(cadre_date, values=annees, width=6, state="readonly")
    annee_combo.grid(row=0, column=2, padx=2)

    # Section Heure
    ttk.Label(fenetre_ajout, text="Heure (HH:MM):").pack(pady=5)
    cadre_heure = tk.Frame(fenetre_ajout, bg="#8B8B7A")
    cadre_heure.pack(pady=5)

    heures = [f"{i:02}" for i in range(24)]
    combobox_heure = ttk.Combobox(cadre_heure, values=heures, width=5, state="readonly")
    combobox_heure.grid(row=0, column=0, padx=2)

    minutes = [f"{i:02}" for i in range(60)]
    combobox_minute = ttk.Combobox(cadre_heure, values=minutes, width=5, state="readonly")
    combobox_minute.grid(row=0, column=1, padx=2)

    # Section Paramètres
    ttk.Label(fenetre_ajout, text="Paramètre:").pack(pady=5)
    parametres = ["Température", "Humidité", "CO2"]
    combobox_parametre = ttk.Combobox(fenetre_ajout, values=parametres, state="readonly")
    combobox_parametre.pack(pady=5)

    ttk.Label(fenetre_ajout, text="Valeur:").pack(pady=5)
    valeur_entree = tk.Entry(fenetre_ajout)
    valeur_entree.pack(pady=5)

    ttk.Label(fenetre_ajout, text="Message prédéfini:").pack(pady=5)
    combobox_message = ttk.Combobox(fenetre_ajout, state="readonly")
    combobox_message.pack(pady=5)

    # Mise à jour des messages prédéfinis en fonction du paramètre sélectionné
    def mettre_a_jour_message(event):#***
        parametre = combobox_parametre.get()
        messages = {
            "Température": ["Température trop élevée", "Température trop basse"],
            "Humidité": ["Humidité trop élevée", "Humidité trop basse"],
            "CO2": ["CO2 trop élevé", "CO2 trop bas"]
        }
        combobox_message["values"] = messages.get(parametre, [])
        combobox_message.set("")

    combobox_parametre.bind("<<ComboboxSelected>>", mettre_a_jour_message)

    # Validation des données et ajout de l'alerte
    def valider_alerte():
        # Récupération des valeurs
        jour = jour_combo.get()
        mois = mois_combo.get()
        annee = annee_combo.get()
        heure = combobox_heure.get()
        minute = combobox_minute.get()
        parametre = combobox_parametre.get()
        valeur = valeur_entree.get()
        message = combobox_message.get()

        # Validation des données
        if not all([jour, mois, annee, heure, minute, parametre, valeur, message]):
            tk.Label(fenetre_ajout, text="Tous les champs doivent être remplis.", fg="red", bg="#8B8B7A").pack(pady=5)
            return

        try:
            valeur_num = float(valeur)
        except ValueError:
            tk.Label(fenetre_ajout, text="La valeur doit être un nombre valide.", fg="red", bg="#8B8B7A").pack(pady=5)
            return

        # Création de la date formatée
        date_str = f"{annee}-{mois}-{jour} {heure}:{minute}"

        # Création du dictionnaire d'alerte
        nouvelle_alerte = {
            "Date": date_str,
            "Parametre": parametre,
            "Valeur": valeur_num,
            "Message": message
        }

        # Sauvegarde dans alerts.json
        alertes_existantes = open_env_data("alerts.json")
        alertes_existantes.append(nouvelle_alerte)
        save_env_data("alerts.json", alertes_existantes)

        rafraichir_alertes(frame_alertes)
        fenetre_ajout.destroy()






