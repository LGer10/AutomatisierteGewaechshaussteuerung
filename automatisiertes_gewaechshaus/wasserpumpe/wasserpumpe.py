from machine import Pin
import time

# define output
p21 = Pin(21, Pin.OUT)

# start pump
p21.value(1)
time.sleep(5)
p21.value(0)