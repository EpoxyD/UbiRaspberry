#!/usr/bin/python

import pifacedigitalio

CHICKS_TOTAL = 9
CHICKS_INSIDE = 0

def switch_pressed(event):
    global CHICKS_INSIDE
    
    event.chip.output_pins[event.pin_num].turn_on()
    if event.pin_num == 0 and pifacedigital.switches[1].value == 0:
        
        while pifacedigital.switches[0].value == 1:
            if pifacedigital.switches[1].value == 1:
                #Chick went inside
                CHICKS_INSIDE = CHICKS_INSIDE + 1

                print "CHICKEN WENT INSIDE: " + str(CHICKS_INSIDE)

                break


    if event.pin_num == 1 and pifacedigital.switches[0].value == 0:

        while pifacedigital.switches[1].value == 1:
            if pifacedigital.switches[0].value == 1:
                #Chick went outside
                CHICKS_INSIDE = CHICKS_INSIDE - 1

                print "CHICKEN WENT OUTSIDE: " + str(CHICKS_INSIDE)

                break



def switch_unpressed(event):
    event.chip.output_pins[event.pin_num].turn_off()
    if event.pin_num == 0:
        BUTTON_0 = 0
    if event.pin_num == 1:
        BUTTON_0 = 0



if __name__ == "__main__":
    
    pifacedigital = pifacedigitalio.PiFaceDigital()

    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)

    for i in range(4):
        listener.register(i, pifacedigitalio.IODIR_ON, switch_pressed)
        listener.register(i, pifacedigitalio.IODIR_OFF, switch_unpressed)

    listener.activate()

