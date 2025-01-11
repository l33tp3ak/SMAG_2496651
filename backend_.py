import json  # Importation du module JSON pour la gestion de la sérialisation et désérialisation des données


# --------------------------- INITIALISATION DE LA BASE DE DONNÉES DES ALERTES ---------------------------

# Cette structure de données sert à stocker les alertes de manière organisée.
# - "alerts_by_time" : Dictionnaire où chaque clé est une heure (format "HH:MM") et la valeur est une alerte associée.

alerts_database = {
    "alerts_by_time": {}   # Initialisation d'un dictionnaire vide pour les alertes par heure
}

# --------------------------- FONCTION : AJOUTER UNE ALERTE PAR HEURE ---------------------------

def add_alert_by_time(hour, parameter, value, message):
    """
    Ajoute une alerte à une heure spécifique dans la base de données des alertes.

    :param hour: Heure à laquelle l'alerte doit être déclenchée (format "HH:MM").
    :param parameter: Le paramètre environnemental concerné (ex. "Température").
    :param value: La valeur seuil du paramètre qui déclenche l'alerte.
    :param message: Message prédéfini décrivant l'alerte.
    """
    # Charger les alertes existantes depuis le fichier JSON
    load_alerts_from_file()

    # Définir ou mettre à jour l'alerte pour l'heure spécifiée
    alerts_database["alerts_by_time"][hour] = {
        "Parameter": parameter,  # Le paramètre concerné par l'alerte
        "Value": value,          # La valeur seuil qui déclenche l'alerte
        "Message": message,      # Message explicatif de l'alerte
        "read": False            # Indique que l'alerte est nouvelle et non encore lue
    }

    # Sauvegarder les alertes mises à jour dans le fichier JSON
    save_alerts_to_file()

# --------------------------- FONCTION : SAUVEGARDER LES ALERTES DANS LE FICHIER JSON ---------------------------

def save_alerts_to_file():
    """
    Sauvegarde la base de données des alertes dans un fichier JSON.
    Cette fonction enregistre les données actuelles de alerts_database dans le fichier.

    """
    with open("alerts.json", "w") as file:
        json.dump(alerts_database, file, indent=4)


# --------------------------- FONCTION : CHARGER LES ALERTES DU FICHIER JSON ---------------------------

def load_alerts_from_file():
    """
    Charge les alertes depuis un fichier JSON dans la variable globale alerts_database.
    Si le fichier n'existe pas ou est mal formé, initialise une structure vide.

    """
    global alerts_database
    try:
        with open("alerts.json", "r") as file:
            alerts_database = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        alerts_database = {"alerts_by_time": {}}  # Structure par défaut

# --------------------------- FONCTION : RÉCUPÉRER LES ALERTES PAR HEURE ---------------------------

def get_alerts_by_time():
    """
    Charge les alertes depuis le fichier JSON et renvoie le dictionnaire des alertes classées par heure.

    :return: Dictionnaire des alertes organisées par heure.
    """

    return alerts_database["alerts_by_time"]  # Retourner le dictionnaire des alertes par heure

# --------------------------- FONCTION : RÉCUPÉRER LES ALERTES NON LUES ---------------------------

def get_unread_alerts():
    """
    Charge les alertes depuis le fichier JSON et renvoie une liste des alertes non lues.

    :return: Liste des alertes dont le champ 'read' est False.
    """
    # Charger les alertes depuis le fichier JSON
    return [
        alert
        for alert in alerts_database["alerts_by_time"].values()
        if not alert.get("read", False)  # Filtrer les alertes non lues
    ]

# --------------------------- INITIALISATION AU DÉMARRAGE DU PROGRAMME ---------------------------

# Charger les alertes dès le démarrage du programme pour s'assurer que alerts_database est à jour
load_alerts_from_file()



#=============================================================================================================
#  si tu veux cette parti pourais etre un autre fichier    backend_trend.py
#=========================================================================================================
import fake_database  # Importation du module back end pour accéder aux données

def get_trend_data(date):
    """
    Récupère les données de tendance pour une date spécifique.

    :param date: Date au format "YYYY-MM-DD" pour laquelle les tendances sont récupérées.
    :return: Dictionnaire contenant les données de température, humidité et CO2 pour la date donnée.
             Si aucune donnée n'est trouvée, retourne un dictionnaire vide.
    """
    data_list = fake_database.tendance_moyenne()  # Récupère la liste des tendances moyennes
    data = next((item for item in data_list if item["Date"] == date), {})
    return data

def get_detailed_trend_data(date):
    """
    Récupère les données détaillées pour une date spécifique.

    :param date: Date au format "YYYY-MM-DD" pour laquelle les données détaillées sont récupérées.
    :return: Dictionnaire contenant les données détaillées par heure.
             Si aucune donnée n'est trouvée, retourne un dictionnaire vide.
    """
    detailed_data = fake_database.get_detailed_data()  # Récupère les données détaillées
    return detailed_data.get(date, {})

# --------------------------- PARTIE 2 : RÉCUPÉRATION DES DONNÉES DE TENDANCE ---------------------------

def update_moyenne(date, trend_labels):
    """
    Met à jour les labels de tendance avec les données récupérées pour une date spécifique.

    :param date: Date au format "YYYY-MM-DD" pour laquelle les tendances sont affichées.
    :param trend_labels: Dictionnaire contenant les widgets Label pour afficher les informations.
    """
    data = get_trend_data(date)  # Récupère les données de tendance pour la date donnée
    trend_labels["date"].config(text=f"Date : {date}")
    trend_labels["temp"].config(text=f"Température : {data.get('Température', 'N/A')}°C")
    trend_labels["humidity"].config(text=f"Humidité : {data.get('Humidité', 'N/A')}%")
    trend_labels["co2"].config(text=f"CO2 : {data.get('CO2', 'N/A')} ppm")


"""Btw Robens, si tu veux, tu pourras seulement garder cette partie intacte et ça pourrait être suffisant. Je me dis que, comme le prof a interdit
 Mongo et que tu dois recommencer, ça pourrait peut-être aller plus vite.

 Il manque juste un petit détail que je n'arrive pas à régler.
Peut-être que tu pourrais travailler dessus : c'est le fait de détecter les "read alerts", pour que, quand une alerte est lue, on puisse
 annuler la notification c'est un truque par raport au boolen a la ligne 38. 

 J'ai envoiller block par block a GPT pour qu'il me commente ca comme un fou haha donc tu peux suprimer ce qui n'es pas utilise , Quoique ca pourrais bien etre utile pour la présentation
 
 Si tu n'es pas à l'aise avec ce code, tu peux le changer : ça te fera une bonne base pour commencer. 
 aussi je vais t'envoiller ma fake data_base tu pourra la prendre comme tienne et si tu en a l'envie tu pourrais esseiller de travailller sur un code qui pourais capter
 les donner a alex de ces sensor en temp real bred tout les nom des fonction fonctione parfaitement avec l'interface donc c'est ca ca pourrais faciliter les chose"""

# Fonction manquante pour afficher l'interface principale qui 
# est ligne 69 pour le moment dans condition_et_gestion.py
########def update_conditions(parameter_frame): #######

