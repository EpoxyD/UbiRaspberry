#!/usr/bin/python

import pifacedigitalio
import time 

pifacedigital = pifacedigitalio.PiFaceDigital()

while True:
    pifacedigital.output_pins[7].turn_on()
    time.sleep(1)
    pifacedigital.output_pins[7].turn_off()
    time.sleep(1)
    pifacedigital.leds[7].turn_on()
    time.sleep(1)
    pifacedigital.leds[7].turn_off()
    time.sleep(1)

