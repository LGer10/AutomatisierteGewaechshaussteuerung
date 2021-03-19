#from machine import Pin
import machine
from time import sleep
import dht

def get_temperature():
    import dht
    from machine import Pin
    # define pin
    sensor = dht.DHT11(Pin(27))

    # measure temperature
    sensor.measure()
    temp = sensor.temperature()
    sleep(5)
    # return temperature
    return '%3.1f' %temp

def get_air_humidity():
    
    # load libraries
    import dht
    from machine import Pin
    
    # define pin
    sensor = dht.DHT11(Pin(27))

    # measure humidity
    sensor.measure()
    hum = sensor.humidity()
    sleep(5)
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
    p0 = Pin(17, Pin.OUT)

    p0.value(1)
    sleep(5)
    p21.value(0)


#control(1,2) 4,16, 17, 18 ,19 , 21, 22,23, 25,26,27,32,33