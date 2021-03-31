from machine import Pin, ADC
import dht
from time import sleep

def get_temperature():

    print("ig bin temp")
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
            print("eine gute Appetit die Storm")
            pass
    
def get_air_humidity():

    print("ig bin humi")
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
            print("eine gute Appetit die Storm")
            pass

def control(pin,status):
    from machine import Pin
    print("ig bin controloer")
    p = Pin(pin, Pin.OUT)

    if(status is "open"):
        p.value(1)
    
    if(status is "close"):
        p.value(0)

def get_brightness():
    print("ig bin hell")
    # define pin
    pot = ADC(Pin(34))
    pot.atten(ADC.ATTN_11DB)
    
    # measure brightness
    pot_value = pot.read()
    
    # return brightness
    return(pot_value)

def get_soil_humidity():
    print("ig bin moisture")
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

def servo():
    print("ig bin servo")
    p4 = machine.Pin(4)
    servo = machine.PWM(p4,freq=50)
    # duty for servo is between 40 - 115
    servo.duty(115)