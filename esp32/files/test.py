import time
#from threading import Threa
import threading
from functions import get_temperature, get_air_humidity,get_soil_humidity, get_brightness

results = {}
def collect(results):
    while True:  
        
        results[0]= ("temperature",get_temperature())
        results[1]= ("humidity", get_air_humidity())
        results[2]= ("brightness", get_brightness())
        results[3]= ("soil_humidity", get_soil_humidity())
        time.sleep(300)
    



thread = threading.Thread(target=collect, args=[results])
thread.start()
time.sleep(20)
print(results[0])
print(results[1])
print(results[2])
print(results[3])
time.sleep(40)
print(results[0])
print(results[1])
print(results[2])
print(results[3])
