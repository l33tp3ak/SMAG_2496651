import json

optimal_thresholds = {
    "Temperature": {"min": 20, "max": 30},
    "Humidite": {"min": 50, "max": 70},
    "Lumiere": {"min": 200, "max": 1000},
    "CO2": {"min": 350, "max": 450}
}

if __name__ == "__main__":
    with open('optimal_thresholds.json', 'w', encoding='utf-8') as thresholds_file:
        json.dump(optimal_thresholds, thresholds_file, indent=4)