#!/usr/bin/python
import pifacedigitalio

pifacedigital = pifacedigitalio.PiFaceDigital()

while True:
    for num in range (0,15):
	pifacedigital.output_pins[0].turn_off()
	pifacedigital.output_pins[1].turn_on()
    pifacedigital.output_pins[2].turn_off()  
	pifacedigital.output_pins[3].turn_off()
	pifacedigital.output_pins[4].turn_off()
	pifacedigital.output_pins[5].turn_off()
	pifacedigital.output_pins[6].turn_off()
	pifacedigital.output_pins[7].turn_off()
    for num in range (0,5):
        pifacedigital.output_pins[0].turn_off()
        pifacedigital.output_pins[1].turn_on()
        pifacedigital.output_pins[2].turn_off()
        pifacedigital.output_pins[3].turn_off()
        pifacedigital.output_pins[4].turn_off()
        pifacedigital.output_pins[5].turn_off()
        pifacedigital.output_pins[6].turn_off()
        pifacedigital.output_pins[7].turn_off()  
