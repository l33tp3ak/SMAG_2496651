import requetes
from colorama import Fore, Style

def afficher_menu():
    print(Fore.GREEN + "\n--- Menu Principal ---" + Style.RESET_ALL)
    print("1. Ajouter les données des capteurs")
    print("2. Afficher les données les plus récentes")
    print("3. Calculer les moyennes des paramètres environnementaux sur une période donnée")
    print("4. Lister toutes les alertes générées avec un filtre sur le paramètre")
    print("5. Analyser les tendances journalières")
    print("6. Trouver le moment avec les conditions les plus optimales")
    print("7. Proposer des actions correctives")
    print("8. Identifier le paramètre le plus problématique")
    print("9. Visualisation: Diagramme en barres interactif")
    print(Fore.RED + "10. Quitter" + Style.RESET_ALL)

def main():
    print("Données des alertes :", requetes.alertes_data)
    print("Données environnementales :", requetes.environment_data)
    print("Données des seuils :", requetes.seuil_data)
    while True:
        afficher_menu()
        choix = input("\nEntrez votre choix (1-10) : ")
        
        if choix == "1":
            requetes.ajouter_donnees_capteurs()
        elif choix == "2":
            requetes.afficher_donnees_recentes()
        elif choix == "3":
            requetes.calculer_moyennes_periode()
        elif choix == "4":
            requetes.lister_alertes_filtrees()
        elif choix == "5":
            requetes.analyser_tendances_journalieres()
        elif choix == "6":
            requetes.trouver_conditions_optimales()
        elif choix == "7":
            requetes.proposer_actions_correctives()
        elif choix == "8":
            requetes.identifier_parametre_problematique()
        elif choix == "9":
            requetes.diagramme_barres_interactif()
        elif choix == "10":
            print(Fore.RED + "Fermeture du programme..." + Style.RESET_ALL)
            break
        else:
            print("Choix invalide, veuillez entrer un nombre entre 1 et 10.")

if __name__ == "__main__":
    main()
