#!/usr/bin/env python
# coding: utf-8

# In[3]:


import time, datetime, calendar, zoneinfo, dateutil, os, json, math


# In[4]:


# Fonction qui libère le terminal de toutes commandes précédentes afin d'afficher le message désiré et demandé dans la charge de travail
# Toutefois, elle ne fonctionne pas dans JupyterLabs, donc pour contourner ce problème ET afficher le message décrit dans la charge de travail, 
def clear():
    screen = os.system("clear||cls")


# In[9]:


def main():
    if os.path.exists("temp.json"):
        print("File exists")
    else:
        """
        Si le fichier n'existe pas, on crée le fichier et ajoute le père noël par défaut.
        Ensuite, on ferme le fichier.
        """
        print("File doesn't exist")
        file = open("temp.json", "w")
        file.close()
    
    temp_dict, humid_dict, light_dict, co2_dict = {
        "serre1": {
            "sensor1":{
                datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"): str(28.5 + "C")
            }
        }
    }, {
        "serre1": {
            "sensor1":{
                datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"): str(84 + "%")
            }
        }
    }, {
        "serre1": {
            "sensor1":{
                datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"): str(620 + " lumen")
            }
        }
    }, {
        "serre1": {
            "sensor1":{
                datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"): str(420 + " ppm")
            }
        }
    }


    acceptable_parameters = {
        "temp": {"min": 19, "max": 24},
        "humid": {"min": 70, "max": 90},
        "light": {"min": 500, "max": 1300},
        "co2": {"min": 200, "max": 500}
    }

    alerts_dict = {
        "temp": {{}},
        "humid": {{}},
        "light": {{}},
        "co2": {{}},
    }


# In[7]:


print(datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"))
# Attend la confirmation de l'utilisateur avant de continuer
input("Appuyer sur Entr\u00E9e pour continuer...")
# Sépare visuellement le message affiché dans JupyterLabs pour correspondre au message dans la charge de travail. Ceci n'a aucun effet dans le programme réel car le terminal est nettoyé durant l'exécution
print("\n\n\n")
clear()


# In[ ]:




