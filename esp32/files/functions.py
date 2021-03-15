#from machine import Pin
import machine
from time import sleep
import dht

def get_temperature():
    import dht
    from machine import Pin
    # define pin
    sensor = dht.DHT11(Pin(4))

    # measure temperature
    sensor.measure()
    temp = sensor.temperature()
    
    # return temperature
    return '%3.1f' %temp

def get_air_humidity():
    
    # load libraries
    import dht
    from machine import Pin
    
    # define pin
    sensor = dht.DHT11(Pin(4))

    # measure humidity
    sensor.measure()
    hum = sensor.humidity()

     # return humidity
    return '%3.1f' %hum

def get_brightness():
    
    # load libraries
    from machine import Pin, ADC
    
    # define pin
    pot = ADC(Pin(34))
    pot.atten(ADC.ATTN_11DB)
    
    # measure brightness
    pot_value = pot.read()
    
    # return brightness
    return(pot_value)


def control(pin,status):

    # load libraries
    from machine import Pin

    # define pin
    p0 = Pin(pin, Pin.OUT)

    p0.value(1)
    sleep(5)
    p21.value(0)


#control(1,2)