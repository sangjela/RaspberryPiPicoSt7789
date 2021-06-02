# 3 LED Blink Run
import machine
import utime
led_onboard = machine.Pin(25, machine.Pin.OUT)
led01 = machine.Pin(1, machine.Pin.OUT)
led14 = machine.Pin(14, machine.Pin.OUT)
onTime = 0.5
offTime = 0.2

while True:
    led_onboard.value(1)
    utime.sleep(onTime)
    led_onboard.value(0)
    utime.sleep(offTime)
    
    led01.value(1)
    utime.sleep(onTime)
    led01.value(0)
    utime.sleep(offTime)

    led14.value(1)
    utime.sleep(onTime)
    led14.value(0)
    utime.sleep(offTime)
