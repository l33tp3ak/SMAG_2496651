# fake_database.py

def get_environment_data():
    """
    Simule l'accès aux données de la base de données (MongoDB ou autre).
    :return: Liste de dictionnaires contenant les données environnementales.
    """
    return [
        {"Date": "2024-12-01 08:00", "Température": 25.0, "Humidité": 60, "Lumière": 300, "CO2": 400},
        {"Date": "2024-12-01 12:00", "Température": 28.0, "Humidité": 55, "Lumière": 800, "CO2": 420},
        {"Date": "2024-12-01 18:00", "Température": 22.5, "Humidité": 65, "Lumière": 500, "CO2": 410},
    ]

