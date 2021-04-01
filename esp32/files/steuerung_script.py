# automatisiertes gewächshaus | main_script | version 0.1

#import json
#import os.path
import time
from threading import Thread
#from datetime import datetime
#from pathlib import Path
import ntptime
from functions import get_temperature, get_air_humidity, get_brightness, get_soil_humidity, control, servo

def get_local_time():

    while True:
        #if needed, overwrite default time server
        ntptime.host = "0.ch.pool.ntp.org"

        try:
            
            ntptime.settime()

            return ((time.localtime()[3]) + 2)
            time.sleep(3600)

        except:
            print("Error syncing time")

    

def control_air_humidity(air_humidity, results_object):
    
    while True:
        
        current_air_humidity = float(results_object.get_result()[1])
        air_humidity = float(air_humidity)
        
        if air_humidity > current_air_humidity:
            print("start floatie")
            control(27,"open")
        
        else:
            print("stop floatie")
            servo("open")
            control(27,"close")
        
        time.sleep(60)


def control_temperature(temperature, results_object):

    while True:
        
        current_temperature = float(results_object.get_result()[0])
        temperature = float(temperature)
        
        if temperature > current_temperature:
            print("start heater")
            control(22,"open")

        
        else:
            print("stop heater")
            control(22,"close")

        
        time.sleep(60)

def control_brightness(brightness, results_object):
    
    while True:

        current_time = get_local_time()
        
        brightness = float(brightness)
        
        if current_time is 8:
            
            time_to_shine = 60
            timeout_start = time.time()
            print("start")

            while time.time() < timeout_start + time_to_shine:
                current_brightness = float(results_object.get_result()[2])
                if current_brightness < 200:
                    print("start light")
                    control(23,"open")
                else:
                    print("stop light")
                    control(23,"close")

            time.sleep(60)

        else:
            time.sleep(60)
            pass
        


def control_soil_humidity(soil_humidity, results_object):

    
    soil_humidity = float(soil_humidity)

    while True:
        current_soil_humidity = float(results_object.get_result()[3])
        if current_soil_humidity < soil_humidity:
            print("start pump")
            control(25,"open")
            time.sleep(5)
            print("stop pump")
            control(25,"close")
        else:
            pass

        
        time.sleep(3600)

def main(temperature, air_humidity, soil_humidity, brightness, results_object):
    
    # initalize temperature thread
    thread_temperature = Thread(target=control_temperature, args=[temperature, results_object])

    # initalize air_humidity thread
    thread_air_humidity = Thread(target=control_air_humidity, args=[air_humidity, results_object])

    # initalize soil_humidity thread
    thread_soil_humidity = Thread(target=control_soil_humidity, args=[soil_humidity,results_object])

     # initalize soil_humidity thread
    thread_brightness = Thread(target=control_brightness, args=[brightness, results_object])

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
