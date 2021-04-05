# automatisiertes gewächshaus | steuerungs_script | version 0.1

# import libraries
import time
from threading import Thread
import ntptime
from functions import get_temperature, get_air_humidity, get_brightness, get_soil_humidity, control, servo

# this function is used to get the current time
def get_local_time():
    
    while True:
        
        # set default time server
        ntptime.host = "0.ch.pool.ntp.org"

        try:
            ntptime.settime()
            
            # since time is returned gmt, we need to add two hours to value (summer time)
            return ((time.localtime()[3]) + 2)
            time.sleep(3600)

        except:
            print("Error syncing time")

    
# this function is used to control the air humidity
def control_air_humidity(air_humidity, results_object):
    
    while True:
        
        # define variables
        current_air_humidity = float(results_object.get_result()[1])
        air_humidity = float(air_humidity)
        
        # compare sensordata with target_value and start or stop floatie accordingly
        if air_humidity > current_air_humidity:
            print("start floatie")
            control(27,"open")
        
        else:
            print("stop floatie")
            control(27,"close")
        
        # sleep 1 minute until checking the values again
        time.sleep(60)

# this function is used to control the temperature
def control_temperature(temperature, results_object):

    while True:
        
        # define variables
        current_temperature = float(results_object.get_result()[0])
        temperature = float(temperature)
        
        # compare sensordata with target_value and start or stop the tubular heater/ servo accordingly
        if temperature > current_temperature:
            print("start heater")
            servo("close")
            control(22,"open")

        else:
            print("stop heater")
            servo("open")
            control(22,"close")

        # sleep 1 minute until checking the values again
        time.sleep(60)

# this function is used to control the brightness
def control_brightness(brightness, results_object):
    
    while True:

        # define variables
        current_time = get_local_time()
        brightness = float(brightness)
        
        # if get_local_time() function returns 8, enter this if statement
        if current_time is 19:
        #if current_time is 8:
            
            # calculate time to shine with target brightness hours
            time_to_shine = 60 * brightness
            
            # define start timer
            timeout_start = time.time()

            # while starter does not reach time to shine, execute commands
            while time.time() < timeout_start + time_to_shine:
                
                # define variables
                current_brightness = float(results_object.get_result()[2])
                
                # if sensordata is below 200, start the lamp
                if current_brightness > 200:
                    print("start light")
                    control(23,"open")
                
                # else stop the lamp
                else:
                    print("stop light")
                    control(23,"close")
                
                # sleep 1 minute until checking the values again
                time.sleep(60)

        # if get_local_time() function does not return 8, wait one hour
        else:
            time.sleep(3600)
            pass
        


def control_soil_humidity(soil_humidity, results_object):

    # define variables
    soil_humidity = float(soil_humidity)

    while True:
        
        # get current sensordata
        current_soil_humidity = float(results_object.get_result()[3])
        
        # compare sensordata with target_value and start for 5 seconds and then stop the pump
        if current_soil_humidity < soil_humidity:
            print("start pump")
            control(25,"open")
            time.sleep(5)
            print("stop pump")
            control(25,"close")
        
        # if target_value is reached continue
        else:
            pass

        # sleep 1 hour until checking the values again
        time.sleep(3600)

def main(temperature, air_humidity, soil_humidity, brightness, results_object):
    
    # initalize temperature thread
    thread_temperature = Thread(target=control_temperature, args=[temperature, results_object])

    # initalize air_humidity thread
    thread_air_humidity = Thread(target=control_air_humidity, args=[air_humidity, results_object])

    # initalize soil_humidity thread
    thread_soil_humidity = Thread(target=control_soil_humidity, args=[soil_humidity,results_object])

     # initalize brightness thread
    thread_brightness = Thread(target=control_brightness, args=[brightness, results_object])

    # start air_humidity thread         
    thread_air_humidity.start()

    # start temperature thread 
    thread_temperature.start()

    # start soil_humidity thread         
    thread_soil_humidity.start()

    # start brightness thread 
    thread_brightness.start()