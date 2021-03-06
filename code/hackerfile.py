#!/usr/bin/python

import sys
import threading
import time
import pifacedigitalio

# Set global variables
chicks_amount   =   9   # total amount of chickens
chicks_inside   =   0   # total amount of chickens currently in the coop
rainbow         =   False

def switch_pressed(event):
    global chicks_inside
    
    event.chip.output_pins[event.pin_num].turn_on()
    if event.pin_num == 0 and pfd.switches[1].value == 0:
        
        while pfd.switches[0].value == 1:
            if pfd.switches[1].value == 1:
                #Chick went inside
                chicks_inside += 1

                print("CHICKEN WENT INSIDE: " + str(chicks_inside))

                break


    if event.pin_num == 1 and pfd.switches[0].value == 0:

        while pfd.switches[1].value == 1:
            if pfd.switches[0].value == 1:
                #Chick went outside
                if chicks_inside > 0:
                    chicks_inside -= 1

                print("CHICKEN WENT OUTSIDE: " + str(chicks_inside))

                break

def switch_unpressed(event):
    event.chip.output_pins[event.pin_num].turn_off()

# Get the amount of chickens in the chicken coop
def get_amount_of_chicks():
    return chicks_amount

# New chickens have arrived, or some have moved to the city. Update the number left in the coop
def set_amount_of_chicks(amount):
    global chicks_amount
    chicks_amount = amount

# Main program, call lots of functions in here, no business logic pls.
if __name__ == "__main__":
    print(get_amount_of_chicks())
    set_amount_of_chicks(12)
    print(get_amount_of_chicks())

    pfd = pifacedigitalio.PiFaceDigital()

    listener = pifacedigitalio.InputEventListener(chip=pfd)

    for i in range(4):
        listener.register(i, pifacedigitalio.IODIR_ON, switch_pressed)
        listener.register(i, pifacedigitalio.IODIR_OFF, switch_unpressed)

    listener.activate()



