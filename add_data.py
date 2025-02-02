import json
import chargement
import random
import os
from chargement import load_optimal_thresholds

seuil = load_optimal_thresholds("seuil.json")  # Récupération centralisée

def get_alerts_count_for_date(alertes_data, date):
    # Extrait juste la date (YYYY-MM-DD) de la timestamp ce qui permet dafficher toute les donnée d'une meme date dans tendance avec lheure séparer pour le graphique
    return sum(1 for alerte in alertes_data if alerte["timestamp"].split()[0] == date)

def struct_add_alerts(paramètre, sensor_data, time):
    seuil = load_optimal_thresholds("optimal_threshold.json")
    alertes_data = chargement.open_env_data("alertes.json")

    
    # Extrait la date du timestamp (YYYY-MM-DD)
    date = time.split()[0]
    
    # Vérifie le nombre d'alertes pour cette date
    alerts_today = get_alerts_count_for_date(alertes_data, date)
    
    # Ne crée une alerte que si on n'a pas dépassé la limite de 2 alertes par jour
    if alerts_today < 2 and (sensor_data < seuil[paramètre]["min"] or sensor_data > seuil[paramètre]["max"]):
        nouvelle_alerte = {
            "timestamp": time,
            "paramètre": paramètre,
            "valeur": sensor_data,
            "status": "active",
            "message": f"{paramètre} {'trop faible' if sensor_data < seuil[paramètre]['min'] else 'trop fort'}"
        }
        
        alertes_data.append(nouvelle_alerte)
        chargement.write_data("alertes.json", alertes_data)
    
    return alertes_data

def generate_sensor_data(seuil):
    return random.randint(seuil["min"] - 10, seuil["max"] + 10)

def auto_sensor_data(selected_date=None):
    seuil = load_optimal_thresholds("optimal_threshold.json")

    
    environment_data = chargement.open_env_data("environment.json")
    
    # Heures fixes pour les 8 mesures (espacées de 3 heures)
    heures = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    
    # Générer 8 mesures
    for heure in heures:
        time = f"{selected_date} {heure}"
        
        nouvelle_mesure = {
            "Date": time,
            "Température": generate_sensor_data(seuil["Température"]),
            "Humidité": generate_sensor_data(seuil["Humidité"]),
            "Lumière": generate_sensor_data(seuil["Lumière"]),
            "CO2": generate_sensor_data(seuil["CO2"])
        }
        
        # Vérifier les alertes pour chaque paramètre
        for paramètre in ["Température", "Humidité", "Lumière", "CO2"]:
            if (nouvelle_mesure[paramètre] < seuil[paramètre]["min"]) or \
               (nouvelle_mesure[paramètre] > seuil[paramètre]["max"]):
                struct_add_alerts(paramètre, nouvelle_mesure[paramètre], time)
        
        environment_data.append(nouvelle_mesure)
    
    chargement.write_data("environment.json", environment_data)
    return environment_data

if __name__ == "__main__":
    environment_data = auto_sensor_data("2024-03-20")  # exemple avec une date fixe
    print("Données environnementales générées :", json.dumps(environment_data, indent=2))