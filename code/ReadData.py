import pifacedigitalio as pfdio

pfdio.init()
def toggle_led0(event):
    print(pfdio.digital_read(7))
def toggle_led1(event):
    event.chip.leds[7].toggle()

pfd = pfdio.PiFaceDigital()
listener = pfdio.InputEventListener(chip=pfd)
listener.register(0, pfdio.IODIR_ON, toggle_led0)
listener.register(1, pfdio.IODIR_ON, toggle_led1)
listener.activate()