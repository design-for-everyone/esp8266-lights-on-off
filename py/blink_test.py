# this file demonstrates blinking a led and is not used in the final application
from machine import Pin
from time import sleep_ms
led = Pin(2,Pin.OUT)
led2 = Pin(5,Pin.OUT)
counter = 0

while True and counter < 5:
    counter = counter + 1
    led.value(1)
    led2.value(0)
    sleep_ms(1500)
    led.value(0)
    led2.value(1)
    sleep_ms(1000)
    
print("done")