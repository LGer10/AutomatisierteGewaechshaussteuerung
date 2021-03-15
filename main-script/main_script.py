# automatisiertes gewächshaus | main_script | version 0.1

import json
import os.path
import time
from threading import Thread
from datetime import datetime
from pathlib import Path
from def_temperature import get_temperature

# variablen deklarieren
current_time = datetime.now().strftime("%H:%M:%S")
start_light_init = 1
running = True

# file deklarieren
file = Path("my_json.json")


def start_light(brightness_hours):
    #time_to_shine = brightness_hours * 60
    time_to_shine = 60
    timeout_start = time.time()

    while time.time() < timeout_start + time_to_shine:
        print("start light")
        print("will sleep for", brightness_hours * 60)
        time.sleep(30)
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

        if ((datetime.now().strftime("%H") == "19") and (start_light_init == 1)):
            start_light_init = 0
            
            thread_start_light = Thread(target=start_light, args=[brightness_hours])
            
            thread_start_light.start()
            
            start_light_init = False
            
            print("initalize Thread")
        
        elif ((datetime.now().strftime("%H") == "19") and (thread_start_light.is_alive())):
            print("Thread läuft")

        else:
            print("Thread fertig")

        if temperature > get_temperature():
            thread_start_heater = Thread(target=start_heater)
            thread_start_heater.start()
        
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


