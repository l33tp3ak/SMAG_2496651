import json
import chargement
import random
import os
import datetime

def get_alerts_count_for_date(alertes_data, date):
	# Extrait juste la date (YYYY-MM-DD) de la timestamp ce qui permet dafficher toute les donnée d'une meme date dans tendance avec lheure séparer pour le graphique
	return sum(1 for alerte in alertes_data if alerte["timestamp"].split()[0] == date)


# Permet d'ajouter une alerte dans le dictionnaire d'alertes et mettre a jour le fichier JSON
def struct_add_alerts(parametre, sensor_data, time = None):
	alertes_data = chargement.open_data("alertes.json")
	seuil = chargement.open_data("optimal_threshold.json")
	if time is None:
		time = datetime.datetime.now().strftime("%d %B %Y %I:%M%p")

	if (alertes_data.get(time) == None):

		alertes_data[time] = {
			parametre: {
				"valeur": sensor_data,
                "status": "active",
                "message": f"{parametre} {'trop faible' if sensor_data < seuil[parametre]['min'] else 'trop fort'}.{'\nRecommendation: Augmentez le chauffage.' if (parametre == 'Température' and sensor_data < seuil[parametre]['min']) else '\nRecommendation: Diminuez le chauffage.' if (parametre == 'Température') else '\nRecommendation: Augmentez irrigation.' if (parametre == 'Humidité' and sensor_data < seuil[parametre]['min']) else '\nRecommendation: Diminuez irrigation.' if (parametre == 'Humidité') else '\nRecommendation: Augmentez intensité des lumières.' if (parametre == 'Lumière' and sensor_data < seuil[parametre]['min']) else '\nRecommendation: Diminuez intensité des lumières.' if (parametre == 'Lumière') else '\nRecommendation: Réduisez la vitesse des ventilateurs.' if (parametre == 'CO2' and sensor_data < seuil[parametre]['min']) else '\nRecommendation: Augmentez la vitesse des ventilateurs.'}"
            }
		}
	else:
		alertes_data[time].update({
			parametre: {
				"valeur": sensor_data,
                "status": "active",
                "message": f"{parametre} {'trop faible' if sensor_data < seuil[parametre]['min'] else 'trop fort'}.{'\nRecommendation: Augmentez le chauffage.' if (parametre == 'Température' and sensor_data < seuil[parametre]['min']) else '\nRecommendation: Diminuez le chauffage.' if (parametre == 'Température') else '\nRecommendation: Augmentez irrigation.' if (parametre == 'Humidité' and sensor_data < seuil[parametre]['min']) else '\nRecommendation: Diminuez irrigation.' if (parametre == 'Humidité') else '\nRecommendation: Augmentez intensité des lumières.' if (parametre == 'Lumière' and sensor_data < seuil[parametre]['min']) else '\nRecommendation: Diminuez intensité des lumières.' if (parametre == 'Lumière') else '\nRecommendation: Réduisez la vitesse des ventilateurs.' if (parametre == 'CO2' and sensor_data < seuil[parametre]['min']) else '\nRecommendation: Augmentez la vitesse des ventilateurs.'}"
           }
		})

	chargement.write_data("alertes.json", alertes_data)
	alertes_data = chargement.open_data("alertes.json")
	#print(alertes_data)
	return alertes_data


def generate_sensor_data(seuil):
	return random.randint(seuil["min"] - 10, seuil["max"] + 10)

def struct_sensor_data(parametre, time = datetime.datetime.now().strftime("%d %B %Y %I:%M%p"), sensor_data = None):
	seuil = chargement.open_data("optimal_threshold.json")
	env_data = chargement.open_data("environment.json")
	# Generate sensor data

	if (sensor_data == None):
		sensor_data = generate_sensor_data(seuil[parametre])
	if (sensor_data < seuil[parametre]["min"]) or (sensor_data > seuil[parametre]["max"]):
		struct_add_alerts(parametre, sensor_data, time)

	if (env_data.get(time) == None):
		env_data[time] = ({parametre: sensor_data})
	else:
		env_data[time].update({parametre: sensor_data})
	chargement.write_data("environment.json", env_data)
	return chargement.open_data("environment.json")


def auto_sensor_data():
	time = datetime.datetime.now().strftime("%d %B %Y %I:%M%p")
	struct_sensor_data("Température", time)
	struct_sensor_data("Humidité", time)
	struct_sensor_data("Lumière", time)
	struct_sensor_data("CO2", time)

	return chargement.open_data("environment.json")

#environment = chargement.open_data("environment.json")
#print(sorted(environment.keys(), key=lambda x: datetime.datetime.strptime(x, "%d %B %Y %I:%M%p"), reverse=True))

"""# Tri des données par heure (comme ranger des livres dans l'ordre)
#filtered_data.sort(key=lambda x: x["Date"].split()[1])                      #************************


environment = chargement.open_data("environment.json")
print(environment)
environment = auto_sensor_data()
for entry in environment:
	print(entry)

date_choisi = f"03 February 2025"  # Création de la date formatée

# Chargement des données depuis le fichier JSON
data = chargement.open_data("environment.json")
filtered_data = []  # Liste vide qu'on va remplir

# Filtrage : on garde seulement les données de la date choisie
for entry in data: # On prend que la partie date ********
	if date_choisi in entry:                                                     #  On regarde si notre donnée est pour notre date choisie
		filtered_data.append(datetime.datetime.strptime(entry, "%d %B %Y %I:%M%p").time())  # Ajout à la liste si ça correspond              #***********

print(filtered_data)

filtered_data.sort()
print(filtered_data)"""