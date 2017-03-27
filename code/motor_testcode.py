#!/usr/bin/python
import pifacedigitalio as pdio

def switch_pressed(event):
    motor_stop()

# BV: het hek moet naar boven
def motor_right():
    print("motor right")
    while pifacedigital.switches[1].value #zo lang de drukknop (switch 1) boven niet ingedrukt wordt
        pifacedigital.output_pins[0].turn_off()
        pifacedigital.output_pins[1].turn_on()
        pifacedigital.output_pins[2].turn_off()
        pifacedigital.output_pins[3].turn_off()
        pifacedigital.output_pins[4].turn_off()
        pifacedigital.output_pins[5].turn_off()
        pifacedigital.output_pins[6].turn_off()
        pifacedigital.output_pins[7].turn_off()

# BV: het hek moet naar beneden
def motor_left():
    print("motor left")
    while pifacedigital.switches[0].value: #zo lang de drukknop beneden niet ingedrukt wordt
        pifacedigital.output_pins[0].turn_on()
        pifacedigital.output_pins[1].turn_off()
        pifacedigital.output_pins[2].turn_off()
        pifacedigital.output_pins[3].turn_off()
        pifacedigital.output_pins[4].turn_off()
        pifacedigital.output_pins[5].turn_off()
        pifacedigital.output_pins[6].turn_off()
        pifacedigital.output_pins[7].turn_off()

def motor_stop():
    print ("motor stop")
    pifacedigital.output_pins[0].turn_off()
    pifacedigital.output_pins[1].turn_off()
    pifacedigital.output_pins[2].turn_off()
    pifacedigital.output_pins[3].turn_off()
    pifacedigital.output_pins[4].turn_off()
    pifacedigital.output_pins[5].turn_off()
    pifacedigital.output_pins[6].turn_off()
    pifacedigital.output_pins[7].turn_off()

if __name__ == "__main__":
    pifacedigital = pifacedigitalio.PiFaceDigital()

    #interrupts
    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    for i in range(4):
        listener.register(i, pifacedigitalio.IODIR_ON, switch_pressed)
        listener.register(i, pifacedigitalio.IODIR_OFF, switch_unpressed)
    listener.activate()
