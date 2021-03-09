# automatisiertes gewächshaus | main_script | version 0.1

import json
import os.path
import time
from threading import Thread
from datetime import datetime
from pathlib import Path
from def_temperature import get_temperature

# file deklarieren
file = Path("my_json.json")
current_time = datetime.now().strftime("%H:%M:%S")
start_light_init = False
running = True

def start_light(brightness_hours):
    print("start light")
    print("will sleep for", brightness_hours * 60)
    time.sleep(brightness_hours * 60)
    print("stop light")

def start_heater():
    print("start heater")
    print("will sleep for 5 sec")
    time.sleep(5)
    print("habe fertig")


# überprüfen ob file existiert
if os.path.isfile(file):
    
    # open json file
    with open(file, 'r') as f:

        json = json.loads(f.read())

    # declare variables    
    id = json["Id"]
    temperature = json["Temperature"]
    brightness_hours = json["brightness_hours"]
    soil_humidity = json["Soil Humidity"]
    air_humidity= json["Air Humidity"]

    while (running == True):
        if datetime.now().strftime("%H") == "22" and start_light_init == False:
            start_light_init == True
            start_light = Thread(target=start_light, args=[brightness_hours]).start()
            print("initalize Thread")
        
        elif datetime.now().strftime("%H") == "22" and start_light.isAlive() == True:
            print("Thread läuft")

        else:
            print("Thread fertig")

        if temperature > get_temperature():
            start_heater = Thread(target=start_heater).start()
        
        print("sleep for 3")
        time.sleep(3)

    current_temp = get_temperature()

    print(id)
    print(temperature)
    print(brightness_hours)
    print(soil_humidity)
    print(air_humidity)
    print(current_temp)

else:
    print("no")


