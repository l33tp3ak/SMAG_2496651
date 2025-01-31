import datetime
import json
import chargement
import random

def struct_add_alerts(parametre, sensor_data, time = None):
	alertes_data = chargement.open_data("alertes.json")
	seuil = chargement.open_data("optimal_threshold.json")
	if time is None:
		time = datetime.datetime.now().strftime("%d %B %Y %I:%M%p")
	if (alertes_data == {}):
		alertes_data = {"active_alerts": [],
						"read_alerts": [],
						"alerts_by_time": {}
						}

	if (alertes_data["alerts_by_time"].get(time) == None):
		if (sensor_data < seuil[parametre]["min"]):
			alertes_data["alerts_by_time"][time] = {
				parametre: {
					"Value": sensor_data, "Message": f"{parametre} trop faible"}
			}
		if (sensor_data > seuil[parametre]["max"]):
			alertes_data["alerts_by_time"][time] = {
				parametre: {
					"Value": sensor_data,
					"Message": f"{parametre} trop fort"}
			}
	else:
		if (sensor_data < seuil[parametre]["min"]):
			alertes_data["alerts_by_time"][time].update({
				parametre: {
					"Value": sensor_data, "Message": f"{parametre} trop faible"}
			})
		if (sensor_data > seuil[parametre]["max"]):
			alertes_data["alerts_by_time"][time].update({
				parametre: {
					"Value": sensor_data,
					"Message": f"{parametre} trop fort"}
			})

	chargement.write_data("alertes.json", alertes_data)
	alertes_data = chargement.open_data("alertes.json")
	print(alertes_data)
	return alertes_data




def generate_sensor_data(seuil):
	return random.randint(seuil["min"] - 10, seuil["max"] + 10)
	

def struct_sensor_data(parametre, time = None):
	seuil = chargement.open_data("optimal_threshold.json")
	env_data = chargement.open_data("environment.json")
	# Generate sensor data
	if (time is None):
		time = datetime.datetime.now().strftime("%d %B %Y %I:%M%p")

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
	struct_sensor_data("Temperature", time)
	struct_sensor_data("Humidite", time)
	struct_sensor_data("Lumiere", time)
	struct_sensor_data("CO2", time)
	
	return chargement.open_data("environment.json")
	


environment_data = chargement.open_data("environment.json")
print(environment_data)
environment_data = auto_sensor_data()
print(environment_data)