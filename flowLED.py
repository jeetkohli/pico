import time
from machine import Pin

LED1 = Pin(1,Pin.OUT)
LED2 = Pin(2,Pin.OUT)
LED3 = Pin(3,Pin.OUT)
LED4 = Pin(4,Pin.OUT)
pause = .2
defled= Pin(25,Pin.OUT)
defled.toggle()
while True:
    LED1.toggle()
    time.sleep(pause)
    LED2.toggle()
    time.sleep(pause)
    LED3.toggle()
    time.sleep(pause)
    LED4.toggle()
    time.sleep(pause)