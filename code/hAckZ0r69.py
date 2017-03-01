#!/usr/bin/python

import sys
import threading
import pifacedigitalio

# Set global variables
chicks_amount   =   9   # total amount of chickens
chicks_inside   =   0   # total amount of chickens currently in the coop
rainbow         =   False
exit_barrier = threading.Barrier(2)

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

def led_enable(event):
    return 0

def deactivate_and_exit(event):
    global exit_barrier
    exit_barrier.wait()

# Main program, call lots of functions in here, no business logic pls.
if __name__ == "__main__":
    print(get_amount_of_chicks())
    set_amount_of_chicks(12)
    print(get_amount_of_chicks())

    pfd = pifacedigitalio.PiFaceDigital()

    listener = pifacedigitalio.InputEventListener(chip=pfd)

    listener.register(0, pifacedigitalio.IODIR_ON, switch_pressed)
    listener.register(1, pifacedigitalio.IODIR_OFF, switch_unpressed)
    listener.register(2,pifacedigitalio.IODIR_ON,led_enable)
    listener.register(3,pifacedigitalio.IODIR_FALLING_EDGE, deactivate_and_exit)

    i = 0
    while i < 10:
        pfd.leds[0].toggle()
        pfd.leds[1].toggle()
        pfd.leds[2].toggle()
        pfd.leds[3].toggle()
        pfd.leds[4].toggle()
        pfd.leds[5].toggle()
        pfd.leds[6].toggle()
        pfd.leds[7].toggle()
        i += 1

    listener.activate()
    exit_barrier.wait()  # program will wait here until exit_barrier releases
    listener.deactivate()
    sys.exit()


