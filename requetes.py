import json
from datetime import datetime
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
from chargement import open_env_data, alertes_data_dump, env_data_dump, seuil_data_dump

# Charger les données des alertes
alertes_data = open_env_data("alertes.json", alertes_data_dump)
env_data_dump = open_env_data("env_data_dump", env_data_dump)
seuil_data_dump = open_env_data("env_data_dump", seuil_data_dump)


# ------------------------- 1. Ajouter les données des capteurs --------------------------

def ajouter_donnees_capteurs():
    """
    Ajoute des données de capteurs manuellement via un widget interactif.
    """
    date_widget = widgets.Text(description="Date (YYYY-MM-DD HH:MM):")
    parametre_widget = widgets.Dropdown(description="Paramètre:", options=["Température", "Humidité", "Lumière", "CO2"])
    valeur_widget = widgets.FloatSlider(description="Valeur:", min=0, max=100, step=0.1)
    message_widget = widgets.Text(description="Message:")

    def on_submit(b):
        date = date_widget.value
        parametre = parametre_widget.value
        valeur = valeur_widget.value
        message = message_widget.value
        alertes_data[date] = {"Paramètre": parametre, "Valeur": valeur, "Message": message}
        with open("alertes.json", "w", encoding="utf-8") as f:
            json.dump(alertes_data, f, ensure_ascii=False)
        print(f"Données ajoutées : {date} - {parametre} - {valeur} - {message}")

    submit_button = widgets.Button(description="Ajouter")
    submit_button.on_click(on_submit)
    display(date_widget, parametre_widget, valeur_widget, message_widget, submit_button)

# ------------------------- 2. Afficher les données les plus récentes --------------------------

def afficher_donnees_recentes():
    """
    Affiche les 5 dernières données environnementales triées par date.
    """
    sorted_data = sorted(alertes_data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M"), reverse=True)
    for date, values in sorted_data[:5]:
        print(f"{date}: {values}")

# ------------------------- 3. Calculer les moyennes des paramètres sur une période donnée --------------------------

def calculer_moyennes_periode():
    """
    Calcule les moyennes des paramètres sur une période sélectionnée via DatePicker.
    """
    start_date_widget = widgets.DatePicker(description="Date de début")
    end_date_widget = widgets.DatePicker(description="Date de fin")

    def on_submit(b):
        start_date = start_date_widget.value
        end_date = end_date_widget.value
        filtered_data = {k: v for k, v in alertes_data.items() if start_date <= datetime.strptime(k, "%Y-%m-%d %H:%M").date() <= end_date}
        moyennes = {"Température": 0, "Humidité": 0, "Lumière": 0, "CO2": 0}
        count = {"Température": 0, "Humidité": 0, "Lumière": 0, "CO2": 0}
        for values in filtered_data.values():
            parametre = values["Paramètre"]
            valeur = values["Valeur"]
            moyennes[parametre] += valeur
            count[parametre] += 1
        for parametre in moyennes:
            if count[parametre] > 0:
                moyennes[parametre] /= count[parametre]
        print(f"Moyennes sur la période {start_date} à {end_date}: {moyennes}")

    submit_button = widgets.Button(description="Calculer")
    submit_button.on_click(on_submit)
    display(start_date_widget, end_date_widget, submit_button)

# ------------------------- 4. Lister toutes les alertes avec un filtre sur le paramètre --------------------------

def lister_alertes_filtrees():
    """
    Liste toutes les alertes générées avec un filtre sur le paramètre via Dropdown.
    """
    parametre_widget = widgets.Dropdown(description="Paramètre:", options=["Température", "Humidité", "Lumière", "CO2"])

    def on_submit(b):
        parametre = parametre_widget.value
        filtered_alertes = {k: v for k, v in alertes_data.items() if v["Paramètre"] == parametre}
        for date, values in filtered_alertes.items():
            print(f"{date}: {values}")

    submit_button = widgets.Button(description="Filtrer")
    submit_button.on_click(on_submit)
    display(parametre_widget, submit_button)

# ------------------------- 5. Analyser les tendances journalières --------------------------

def analyser_tendances_journalieres():
    """
    Analyse les tendances journalières pour un paramètre donné.
    """
    date_widget = widgets.DatePicker(description="Date:")
    parametre_widget = widgets.Dropdown(description="Paramètre:", options=["Température", "Humidité", "Lumière", "CO2"])

    def on_submit(b):
        date = date_widget.value
        parametre = parametre_widget.value
        filtered_data = {k: v for k, v in alertes_data.items() if datetime.strptime(k, "%Y-%m-%d %H:%M").date() == date and v["Paramètre"] == parametre}
        for time, values in filtered_data.items():
            print(f"{time}: {values}")

    submit_button = widgets.Button(description="Analyser")
    submit_button.on_click(on_submit)
    display(date_widget, parametre_widget, submit_button)

# ------------------------- 6. Trouver le moment avec les conditions les plus optimales --------------------------

def trouver_conditions_optimales():
    """
    Trouve le moment avec les conditions les plus optimales.
    """
    seuils_optimaux = {"Température": 22.0, "Humidité": 60.0, "Lumière": 500.0, "CO2": 800.0}
    scores = {}
    for date, values in alertes_data.items():
        parametre = values["Paramètre"]
        valeur = values["Valeur"]
        ecart = abs(valeur - seuils_optimaux[parametre])
        if date in scores:
            scores[date] += ecart
        else:
            scores[date] = ecart
    meilleure_date = min(scores, key=scores.get)
    print(f"Conditions optimales le {meilleure_date}: {alertes_data[meilleure_date]}")

# ------------------------- 7. Proposer des actions correctives --------------------------

def proposer_actions_correctives():
    """
    Propose des actions correctives en fonction des alertes générées.
    """
    actions = {
        "Température": {
            "trop élevée": "Réduire la température (augmenter la ventilation)",
            "trop basse": "Augmenter la température (réduire la ventilation)"
        },
        "Humidité": {
            "trop élevée": "Réduire l'humidité (augmenter la ventilation)",
            "trop basse": "Ajouter de l'humidité (augmenter l'irrigation)"
        },
        "Lumière": {
            "trop élevée": "Réduire l'éclairage",
            "trop basse": "Augmenter l'éclairage"
        },
        "CO2": {
            "trop élevé": "Augmenter la ventilation",
            "trop bas": "Réduire la ventilation"
        }
    }
    for date, values in alertes_data.items():
        parametre = values["Paramètre"]
        valeur = values["Valeur"]
        if parametre in actions:
            if "trop élevé" in values["Message"]:
                print(f"{date}: {actions[parametre]['trop élevée']}")
            elif "trop bas" in values["Message"]:
                print(f"{date}: {actions[parametre]['trop basse']}")

# ------------------------- 8. Identifier le paramètre le plus problématique --------------------------

def identifier_parametre_problematique():
    """
    Identifie le paramètre le plus problématique sur une période donnée.
    """
    start_date_widget = widgets.DatePicker(description="Date de début")
    end_date_widget = widgets.DatePicker(description="Date de fin")

    def on_submit(b):
        start_date = start_date_widget.value
        end_date = end_date_widget.value
        filtered_alertes = {k: v for k, v in alertes_data.items() if start_date <= datetime.strptime(k, "%Y-%m-%d %H:%M").date() <= end_date}
        compteur = {"Température": 0, "Humidité": 0, "Lumière": 0, "CO2": 0}
        for values in filtered_alertes.values():
            parametre = values["Paramètre"]
            compteur[parametre] += 1
        parametre_problematique = max(compteur, key=compteur.get)
        print(f"Le paramètre le plus problématique est {parametre_problematique} avec {compteur[parametre_problematique]} alertes.")

    submit_button = widgets.Button(description="Identifier")
    submit_button.on_click(on_submit)
    display(start_date_widget, end_date_widget, submit_button)

# ------------------------- 9. Diagramme en barres interactif --------------------------

def diagramme_barres_interactif():
    """
    Affiche un diagramme en barres interactif des moyennes journalières des paramètres.
    """
    parametre_widget = widgets.Dropdown(description="Paramètre:", options=["Température", "Humidité", "Lumière", "CO2"])

    def on_submit(b):
        parametre = parametre_widget.value
        dates = sorted(set(datetime.strptime(k, "%Y-%m-%d %H:%M").date() for k in alertes_data.keys()))
        moyennes = []
        for date in dates:
            valeurs = [v["Valeur"] for k, v in alertes_data.items() if datetime.strptime(k, "%Y-%m-%d %H:%M").date() == date and v["Paramètre"] == parametre]
            if valeurs:
                moyennes.append(sum(valeurs) / len(valeurs))
            else:
                moyennes.append(0)
        plt.bar(dates, moyennes)
        plt.xlabel("Date")
        plt.ylabel(f"Moyenne {parametre}")
        plt.title(f"Moyennes journalières de {parametre}")
        plt.show()

    submit_button = widgets.Button(description="Afficher")
    submit_button.on_click(on_submit)
    display(parametre_widget, submit_button)

# ------------------------- Visualisation d'un Diagramme en lignes --------------------------

def diagramme_lignes_interactif():
    """
    Affiche un diagramme en lignes interactif de l'évolution d'un paramètre sur une période donnée.
    """
    parametre_widget = widgets.Dropdown(description="Paramètre:", options=["Température", "Humidité", "Lumière", "CO2"])
    start_date_widget = widgets.DatePicker(description="Date de début")
    end_date_widget = widgets.DatePicker(description="Date de fin")

    def on_submit(b):
        parametre = parametre_widget.value
        start_date = start_date_widget.value
        end_date = end_date_widget.value
        filtered_data = {k: v for k, v in alertes_data.items() if start_date <= datetime.strptime(k, "%Y-%m-%d %H:%M").date() <= end_date and v["Paramètre"] == parametre}
        dates = sorted(datetime.strptime(k, "%Y-%m-%d %H:%M") for k in filtered_data.keys())
        valeurs = [filtered_data[k.strftime("%Y-%m-%d %H:%M")]["Valeur"] for k in dates]
        plt.plot(dates, valeurs)
        plt.xlabel("Date")
        plt.ylabel(parametre)
        plt.title(f"Évolution de {parametre} sur la période {start_date} à {end_date}")
        plt.show()

    submit_button = widgets.Button(description="Afficher")
    submit_button.on_click(on_submit)
    display(parametre_widget, start_date_widget, end_date_widget, submit_button)