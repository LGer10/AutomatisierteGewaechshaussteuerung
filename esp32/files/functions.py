# automatisiertes gewächshaus | function library | version 0.1

# import libraries
from machine import Pin, ADC, PWM
import dht
from time import sleep

# this function is used to get the current temperature
def get_temperature():

    # print message for debug reasons
    print("reading temperature")
    
    # define pin and activate PULL_UP Resistor
    sensor = dht.DHT11(Pin(21, Pin.PULL_UP))

    # define variable
    temp = None

    while temp is None:
        
        # sleep 3 seconds, since sensor could still be used by other a function
        sleep(3)
        
        try:
            
            # sleep two seconds to make sure, sensor is not used
            sleep(2)

            # measure temperature
            sensor.measure()
            temp = sensor.temperature()
            
            # return temperature
            return '%3.1f' %temp

        # in case of failure print debug message and continue loop
        except OSError as e:
            print("Error reading sensor data")
            pass

# this function is used to get the current humidity    
def get_air_humidity():

    # print message for debug reasons
    print("reading humidity")
    
    # define pin and activate PULL_UP Resistor
    sensor = dht.DHT11(Pin(21, Pin.PULL_UP))

    # define variable
    hum = None
    
    while hum is None:
        
        # sleep 3 seconds, since sensor could still be used by other a function
        sleep(3)
        
        try:

            # sleep two seconds to make sure, sensor is not used 
            sleep(2)
            
            # measure humidity
            sensor.measure()
            hum= sensor.humidity()
            
            # return humidity
            return '%3.1f' %hum

        # in case of failure print debug message and continue loop
        except OSError as e:
            print("Error reading sensor data")
            pass

# this function is used to control the outputs of the satellite
def control(pin,status):

    # define pin
    p = Pin(pin, Pin.OUT)

    # if argument is "open" set pin value to 0
    if(status is "open"):
        p.value(0)
    
    # if argument is "close" set pin value to 1
    if(status is "close"):
        p.value(1)

# this function is used to get the current brightness 
def get_brightness():
    
    # print message for debug reasons
    print("reading brightness")
    
    # define pin as analog pin
    pot = ADC(Pin(34))
    pot.atten(ADC.ATTN_11DB)
    
    # measure brightness
    pot_value = pot.read()
    
    # return brightness
    return(pot_value)

# this function is used to get the current soilhumidity
def get_soil_humidity():
    
    # print message for debug reasons
    print("reading soilhumidity")
    
    # voll nass = 1449.0
    # voll trocken = 4095
    
    # define pin
    pot = ADC(Pin(36))
    pot.atten(ADC.ATTN_11DB)

    # prepare while loop for measure 10 sample to avoid noise
    i = 0

    while i < 10:
        
        # measure soil_humidity
        moisture = pot.read()
        
        # define array
        list = []
        
        # add measurement to array
        list.append(moisture)

        # increment i
        i += 1
        
        # sleep half a second
        sleep(0.5)
        
    # define number_list as list  
    number_list = list
    
    # calculate average
    avg = sum(number_list)/len(number_list)
    wert = (round(avg,2))

    if wert > 4000:
        return(0)
    else:
        percent = ((4095 - wert) / 2646 ) * 100

        return(percent)

def servo(status):

    # define pin
    p4 = Pin(4)
    servo = PWM(p4,freq=50)

    if(status is "open" and servo.duty() is not 40):
        servo.duty(40)

    if(status is "close" and servo.duty() is not 115):
        servo.duty(115)

