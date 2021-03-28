from machine import Pin, ADC
import dht
from time import sleep

def get_temperature():

    # define pin
    sensor = dht.DHT11(Pin(21))

    temp = None

    while temp is None:
        try:
            
            sleep(3)

            # measure temperature
            sensor.measure()
            temp = sensor.temperature()
            
            # return temperature
            return '%3.1f' %temp
        
        except OSError as e:
            pass
    
def get_air_humidity():

    # define pin
    sensor = dht.DHT11(Pin(21))

    hum = None
    
    while hum is None:
        try:

            sleep(3)
            
            # measure humidity
            sensor.measure()
            hum= sensor.humidity()
            
            # return humidity
            return '%3.1f' %hum

        except OSError as e:
            pass

def control(pin,status):
    from machine import Pin

    p = Pin(pin, Pin.OUT)

    if(status is "open"):
        p.value(1)
    
    if(status is "close"):
        p.value(0)

def get_brightness():
    
    # define pin
    pot = ADC(Pin(34))
    pot.atten(ADC.ATTN_11DB)
    
    # measure brightness
    pot_value = pot.read()
    
    # return brightness
    return(pot_value)

def get_soil_humidity():
    # voll nass = 1449.0
    # voll trocken = 4095
    
    # define pin
    pot = ADC(Pin(36))
    pot.atten(ADC.ATTN_11DB)

    i = 0

    while i < 10:
        
        # measure soil_humidity
        moisture = pot.read()
        
        # define array
        list = []
        
        # add measurement to array
        list.append(moisture)

        i += 1
        sleep(0.5)
        
        
    number_list = list
    avg = sum(number_list)/len(number_list)
    wert = (round(avg,2))

    if wert > 4000:
        return(0)
    else:
        percent = ((4095 - wert) / 2646 ) * 100

        return(percent)