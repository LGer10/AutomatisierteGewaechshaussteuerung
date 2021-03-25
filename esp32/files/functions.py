import machine

import dht


def get_temperature():
    
    #import dht
    import dht
    from machine import Pin
    from time import sleep

    # define pin
    sensor = dht.DHT11(Pin(21))
    while True:
    # measure temperature
    
        try:

            sleep(10)
            sensor.measure()

            temp = sensor.temperature()
            return '%3.1f' %temp
    
        except OSError as e:
            print('Failed to read sensor.')
    
    # return temperature



def get_air_humidity():
    import dht
    from machine import Pin
    from time import sleep

    # load libraries
    #import dht
    #from machine import Pin
    sensor = dht.DHT11(Pin(21))
    
    while True:
        try:
            # define pin
            sleep(10)
            # measure humidity
            sensor.measure()
            hum = sensor.humidity()
            
            # return humidity
            return '%3.1f' %hum

        except OSError as e:
            print('Failed to read sensor humidity.')
     



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
    from machine import Pin

    p = Pin(pin, Pin.OUT)

    if(status is "open"):
        p.value(1)
    
    if(status is "close"):
        p.value(0)

#control(1,2) 4,16, 7, 18 ,19 , 21, 22,23, 25,26,27,32,33

