# automatisiertes gewächshaus | main_script | version 0.1

#import json
#import os.path
import time
from threading import Thread
#from datetime import datetime
#from pathlib import Path
import functions


temperature = 25
air_humidity = 55

def control_air_humidity(air_humidity):
    
    while True:
        
        if functions.get_air_humidity() < str(air_humidity):
            print("start floatie")
            functions.control(22,"close")
        
        else:
            print("open doors")
            functions.control(22,"open")

        time.sleep(5)



def control_temperature(temperature):
    
    while True:
        
        temperature = functions.get_temperature()
        temperature = float(temperature)

        if float(functions.get_temperature()) < float(temperature):
            print("start heater")
            functions.control(19,"open")
        
        else:
            print("stop heater")
            functions.control(19,"close")

        time.sleep(30)


def main(temperature, air_humidity, soil_humidity, brightness):
    print(temperature)
    print(air_humidity)
    print(soil_humidity)
    print(brightness)


    # initalize temperature thread
    thread_temperature = Thread(target=control_temperature, args=[temperature])

    # initalize air_humidity thread
    thread_air_humidity = Thread(target=control_air_humidity, args=[air_humidity])

    # initalize soil_humidity thread
    thread_soil_humidity = Thread(target=control_temperature, args=[soil_humidity])

     # initalize soil_humidity thread
    thread_brightness = Thread(target=control_temperature, args=[brightness])

    # start air_humidity thread         
    thread_air_humidity.start()

    # start temperature thread 
    thread_temperature.start()

    # start soil_humidity thread         
    thread_soil_humidity.start()

    # start brightness thread 
    thread_brightness.start()
            


"""

thread_air_humidity = Thread(target=control_air_humidity, args=[air_humidity])
            
thread_air_humidity.start()

thread_temperature = Thread(target=control_temperature, args=[control_temperature])
            
thread_temperature.start()


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

"""
