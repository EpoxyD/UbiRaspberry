#!/usr/bin/python

#import pifacedigitalio
import sys
import threading
import time
import datetime
import time
import pymysql
import requests
import json

# Set global variables
chicks_amount   =   4   # total amount of chickens
chicks_inside   =   0   # total amount of chickens currently in the coop
sunrise_today = int(time.time())
sunset_today = int(time.time())
sunrise_tomorrow = int(time.time())
sunset_tomorrow = int(time.time())
current_time = int(time.time())
sun_down = True

# Functions

def switch_pressed(event):
    if event.pin_num == 0 or event.pin_num == 1: #chicken inside or outside
        count_chicks(event)

    if event.pin_num == 2 or event.pin_num == 3: #poort is boven of beneden
        motor_stop()

# BV: het hek moet naar beneden
def motor_right():
    print("motor right")
    pifacedigital.output_pins[0].turn_off() #enable ON
    while pifacedigital.switches[3].value == 0: #zo lang de drukknop (switch 4) beneden niet ingedrukt wordt
        pifacedigital.output_pins[1].turn_off()
        pifacedigital.output_pins[2].turn_on()
        pifacedigital.output_pins[3].turn_on()
        pifacedigital.output_pins[4].turn_on()
        pifacedigital.output_pins[5].turn_on()
        pifacedigital.output_pins[6].turn_on()
        pifacedigital.output_pins[7].turn_on()

# BV: het hek moet naar boven
def motor_left():
    print("motor left")
    pifacedigital.output_pins[0].turn_off() #enable ON
    while pifacedigital.switches[2].value == 0: #zo lang de drukknop (switch 3) boven niet ingedrukt wordt
        pifacedigital.output_pins[1].turn_on()
        pifacedigital.output_pins[2].turn_off()
        pifacedigital.output_pins[3].turn_on()
        pifacedigital.output_pins[4].turn_on()
        pifacedigital.output_pins[5].turn_on()
        pifacedigital.output_pins[6].turn_on()
        pifacedigital.output_pins[7].turn_on()

def motor_stop():
    print ("motor stop")
    pifacedigital.output_pins[0].turn_on() #enable OFF
    pifacedigital.output_pins[1].turn_n()
    pifacedigital.output_pins[2].turn_on()
    pifacedigital.output_pins[3].turn_on()
    pifacedigital.output_pins[4].turn_on()
    pifacedigital.output_pins[5].turn_on()
    pifacedigital.output_pins[6].turn_on()
    pifacedigital.output_pins[7].turn_on()

def count_chicks(event):
    global chicks_inside

    if event.pin_num == 0 and pifacedigital.switches[1].value == 0:

        while pifacedigital.switches[0].value == 1:
            if pifacedigital.switches[1].value == 1:
                #Chick went inside
                chicks_inside += 1
                print("CHICKEN WENT INSIDE: " + str(chicks_inside))
                if chicks_inside == chicks_amount and sun_down == True:
                    motor_right();

                break


    if event.pin_num == 1 and pifacedigital.switches[0].value == 0:

        while pifacedigital.switches[1].value == 1:
            if pifacedigital.switches[0].value == 1:
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
def set_amount_of_chicks():
    #On pi
    #conn = pymysql.connect(host='localhost', user='root', passwd='root', db='ChickCounter')
    #From laptop
    conn = pymysql.connect(host='192.168.0.104', user='root', passwd='root', db='ChickCounter')

    cur = conn.cursor()
    cur.execute("SELECT * FROM ChickCounter.chickens")
    total_chicks = 0
    for response in cur:
        total_chicks = total_chicks + 1
        print(response)

    print("total_chicks: " + str(total_chicks))
    cur.close()

    global chicks_amount
    chicks_amount = total_chicks

def set_sun_time():
    r = requests.get('https://api.darksky.net/forecast/a22f23bee010f3976f614a0460d1ccf6/50.87296604411913,4.697816732888441')
    json_response = json.dumps(r.json(), ensure_ascii=False)
    json_today = json.loads(json_response)['daily']['data'][0]
    json_tomorrow = json.loads(json_response)['daily']['data'][1]

    datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')

    #unix timestamp
    global sunrise_today, sunset_today, current_time
    sunrise_today = json_today['sunriseTime']
    sunset_today = json_today['sunsetTime']
    sunrise_tomorrow = json_tomorrow['sunriseTime']
    sunset_tomorrow = json_tomorrow['sunsetTime']
    current_time = json.loads(json_response)['currently']['time']

    #datetime
    print ("sunrise today: " + str(datetime.datetime.fromtimestamp(int(sunrise_today)).strftime('%Y-%m-%d %H:%M:%S')))
    print ("sunset today: " + str(datetime.datetime.fromtimestamp(int(sunset_today)).strftime('%Y-%m-%d %H:%M:%S')))
    print ("sunrise tomorrow: " + str(datetime.datetime.fromtimestamp(int(sunrise_tomorrow)).strftime('%Y-%m-%d %H:%M:%S')))
    print ("sunset tomorrow: " + str(datetime.datetime.fromtimestamp(int(sunset_tomorrow)).strftime('%Y-%m-%d %H:%M:%S')))
    print ("current time: " + str(datetime.datetime.fromtimestamp(int(current_time)).strftime('%Y-%m-%d %H:%M:%S')))

def sun_down():
    global sun_down
    print(sunrise_today)
    print(current_time)
    print(sunset_today)
    
    if sunrise_today < current_time and current_time < sunset_today:
        print("sun is up")
        sun_down = False
    else:
        print("sun is down")
        sun_down = True


if __name__ == "__main__":
    set_amount_of_chicks()  #check in DB the amount of chicks
    set_sun_time()  #check current time and sunset, sunrise time, set global var
    sun_down()  #check if it's dark or not -> set global var sun_down

    print(get_amount_of_chicks())

    pifacedigital = pifacedigitalio.PiFaceDigital()

    #interrupts
    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    for i in range(4):
        listener.register(i, pifacedigitalio.IODIR_ON, switch_pressed)
        listener.register(i, pifacedigitalio.IODIR_OFF, switch_unpressed)

    listener.activate()
