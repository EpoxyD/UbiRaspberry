#!/usr/bin/python

import sys
import threading as thd
import pifacedigitalio as pdio
import datetime

exit_barrier = thd.Barrier(2)       # Escape from program with ctrl-c
gate_state = False


# Function to exit on button press
def quit_hok(event):
    global exit_barrier
    print("Bye Bye")
    exit_barrier.wait()


# Read the current input values
def read_data(event):
    print("DATA AT " + str(datetime.datetime.utcnow()))
    print("Pin 5 = " + str(pfd.input_pins[4].value))
    print("Pin 6 = " + str(pfd.input_pins[5].value))
    print("Pin 7 = " + str(pfd.input_pins[6].value))
    print("Pin 8 = " + str(pfd.input_pins[7].value))


# A chicken has passed the first IR_LED
def ir_led_1(event):
    print("Chicken passed LED 1")
    #TODO Implement Counting Logic


# A chicken has passed the second IR_LED
def ir_led_2(event):
    print("Chicken passed LED 2")
    #TODO Implement Counting Logic


# The gate was fully opened
def gate_opened(event):
    print("The gate is now open!")
    global gate_state
    gate_state = True

# The gate was fully closed
def gate_closed(event):
    print("The gate is now closed!")
    global gate_state
    gate_state = False

# The gate opens now
def gate_action_open(event):
    print("The gat is opening...")

# The gate closes  now
def gate_action_close(event):
    print("The gat is closing...")

# Main program, call lots of functions in here, no business logic pls.
if __name__ == "__main__":
    pdio.init()
    pfd = pdio.PiFaceDigital()
    listener = pdio.InputEventListener(chip=pfd)
    listener.register(0, pdio.IODIR_FALLING_EDGE, quit_hok)
    listener.register(1, pdio.IODIR_FALLING_EDGE, read_data)
    listener.register(7, pdio.IODIR_FALLING_EDGE, ir_led_1)
    listener.register(5, pdio.IODIR_FALLING_EDGE, ir_led_2)
    listener.register(6, pdio.IODIR_FALLING_EDGE, gate_opened)
    listener.register(7, pdio.IODIR_FALLING_EDGE, gate_closed)
    listener.activate()
    exit_barrier.wait()    # Program waits until barrier releases
    listener.deactivate()
    sys.exit()
