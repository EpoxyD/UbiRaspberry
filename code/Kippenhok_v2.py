#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import http.server
import json
import pifacedigitalio as pdio
import pymysql
import os
import requests
import spidev
import subprocess
import sys
import time
import threading as thd
import urllib.parse

from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonpify

# OUTPUT PORTS
MOTOR_ENABLE = 0
MOTOR_STEER_1 = 1
MOTOR_STEER_2 = 2

# INPUT PORTS
MOTOR_DOWN = 1
MOTOR_UP = 2
        
# SPI Variables
INFRARED_LED_SPI0 = 1
INFRARED_LED_SPI1 = 7
pot_level0 = 0
pot_level1 = 0
READING_DELAY = 1

# General Variables
GATE_LED_BOOL1 = False
GATE_LED_BOOL2 = False

# Flask Api Variables
app = Flask(__name__)
api = Api(app)
TOTAL_CHICKS_INSIDE = 0
TOTAL_CHICKS_AMOUNT = 0
sunrise_today = None
sunset_today = None
sunrise_tomorrow = None
sunset_tomorrow = None
current_time = None
sun_down = True
gate_state = True
threadrun = None

# MUTEX
mutex = thd.Lock()

# Setup code
spi = spidev.SpiDev()
spi.open(0, 1)

# Get Chickens_Amount
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='ChickCounter')
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM chickens")
TOTAL_CHICKS_AMOUNT = cursor.fetchone()[0]


# Gate Class for Flask API
class Gate(Resource):
    def get(self,gate_command):
        global gate_state
        if gate_command == 'open':
            gate_state = True
        if gate_command == 'close':
            gate_state = False
        return gate_state

# Return Chicken class to website
class Total_Chicks_Inside(Resource):
    def get(self):
        global TOTAL_CHICKS_INSIDE
        print("Total Chicks Inside:" + str(TOTAL_CHICKS_INSIDE))
        return jsonpify({'TotalChicksInside':TOTAL_CHICKS_INSIDE})

# Change the total amount of chickens
class Change_Chick_amount(Resource):
    def get(self, total_chicks):
        global TOTAL_CHICKS_AMOUNT
        
        if total_chicks == 'add':
            TOTAL_CHICKS_AMOUNT = TOTAL_CHICKS_AMOUNT + 1
            print("total chicks + 1")
        elif total_chicks == 'remove':
            TOTAL_CHICKS_AMOUNT = TOTAL_CHICKS_AMOUNT - 1
            print("total chicks - 1")
        
        return {'total_chicks': TOTAL_CHICKS_AMOUNT}

    
# Read SPI channel
def ReadChannel(channel):
    mutex.acquire()
    try:
        adc = spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
    finally:
        mutex.release()
    return data

# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data, places):
    volts = (data * 3.3) / float(1023)
    volts = round(volts, places)
    return volts

def read_data(event):
    print('DATA AT ' + str(datetime.datetime.utcnow()))
    print('Pin 5 = ' + str(pfd.input_pins[4].value))
    print('Pin 6 = ' + str(pfd.input_pins[5].value))
    print('Pin 7 = ' + str(pfd.input_pins[6].value))
    print('Pin 8 = ' + str(pfd.input_pins[7].value))

'''
# BV: het hek moet naar beneden
def motor_down(event):
    print("motor down")
    while pfd.input_pins[MOTOR_DOWN].value == 1:
        pfd.output_pins[MOTOR_ENABLE].turn_off() #enable ON
        pfd.output_pins[MOTOR_STEER_1].turn_off()
        pfd.output_pins[MOTOR_STEER_2].turn_on()
    motor_stop()

# BV: het hek moet naar boven
def motor_up():
    #while pfd.input_pins[MOTOR_UP].value == 1:    
    while gate_state == False:
        for num in range(0,25):
            pfd.output_pins[MOTOR_ENABLE].turn_off() #enable ON
            pfd.output_pins[MOTOR_STEER_1].turn_off()
            pfd.output_pins[MOTOR_STEER_2].turn_on()
        for num in range(0,10):
            pfd.output_pins[MOTOR_ENABLE].turn_on() #enable ON
            pfd.output_pins[MOTOR_STEER_1].turn_on()
            pfd.output_pins[MOTOR_STEER_2].turn_on()
    while gate_state == True:
    pfd.output_pins[MOTOR_ENABLE].turn_on() #enable OFF
    pfd.output_pins[MOTOR_STEER_1].turn_on()
    pfd.output_pins[MOTOR_STEER_2].turn_on()
        
def motor_stop():
    pfd.output_pins[MOTOR_ENABLE].turn_on() #enable OFF
    pfd.output_pins[MOTOR_STEER_1].turn_on()
    pfd.output_pins[MOTOR_STEER_2].turn_on()
'''

# Retreive sun data
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
    print ("sunset tomorrow: " + str(datetime.datetime.fromtimestamp(int(sunset_tomorrow)).strftime('%Y-%m-%d H:%M:%S')))
    print ("current time: " + str(datetime.datetime.fromtimestamp(int(current_time)).strftime('%Y-%m-%d %H:%M:%S')))
    
# Return boolean about the sun being down or not
def sun_down():
    global sun_down
    if sunrise_today < current_time and current_time < sunset_today:
        print("sun is up")
        sun_down = False
    else:
        print("sun is down")
        sun_down = True

# Check for chicken in
def chick_in():
    global TOTAL_CHICKS_INSIDE
    global gate_state
    while (GATE_LED_BOOL1 == 0) and (GATE_LED_BOOL2 == 1):
        while (GATE_LED_BOOL1 == 1) and (GATE_LED_BOOL2 == 1):
            while (GATE_LED_BOOL1 == 1) and (GATE_LED_BOOL2 == 0):
                if (GATE_LED_BOOL1 == 0) and (GATE_LED_BOOL2 == 0):
                    # Count chick inside
                    TOTAL_CHICKS_INSIDE = TOTAL_CHICKS_INSIDE + 1
                    print("CHICKEN WENT INSIDE: " + str(TOTAL_CHICKS_INSIDE))
                    if TOTAL_CHICKS_INSIDE == TOTAL_CHICKS_AMOUNT and sun_down == True:
                        gate_state = True
                    break
            if (GATE_LED_BOOL1 == 0) and (GATE_LED_BOOL2 == 0):
                print("NOOPE")
                break
        if (GATE_LED_BOOL1 == 0) and (GATE_LED_BOOL2 == 0):
            print("NOPE")
            break
    
# Check for chicken out
def chick_out():
    global TOTAL_CHICKS_INSIDE
    global gate_state
    while (GATE_LED_BOOL1 == 1) and (GATE_LED_BOOL2 == 0):
        while (GATE_LED_BOOL1 == 1) and (GATE_LED_BOOL2 == 1):
            while (GATE_LED_BOOL1 == 0) and (GATE_LED_BOOL2 == 1):
                if (GATE_LED_BOOL1 == 0) and (GATE_LED_BOOL2 == 0):
                    # Count chick inside
                    TOTAL_CHICKS_INSIDE = TOTAL_CHICKS_INSIDE - 1
                    print("CHICKEN WENT OUTSIDE: " + str(TOTAL_CHICKS_INSIDE))
                    gate_state = False
                    break
            if (GATE_LED_BOOL1 == 0) and (GATE_LED_BOOL2 == 0):
                break
        if (GATE_LED_BOOL1 == 0) and (GATE_LED_BOOL2 == 0):
            break  
            
# Set boolean if infrared is triggered
def set_LED_bool1(event):
    global GATE_LED_BOOL1
    print('Change BOOL1')
    GATE_LED_BOOL1 = not GATE_LED_BOOL1

# Set boolean if infrared is triggered
def set_LED_bool2(event):
    global GATE_LED_BOOL2
    print('Change BOOL2')
    GATE_LED_BOOL2 = not GATE_LED_BOOL2

# Get the amount of chickens in the chicken coop
def get_chicks_inside():
    return TOTAL_CHICKS_INSIDE

# Get the total amount of chickens in the chicken coop
def get_chicks_inside():
    return TOTAL_CHICKS_AMOUNT

def count_chicks(event):
    global chicks_inside
    if event.pin_num == 0 and pifacedigital.switches[1].value == 0:
        while pfd.switches[0].value == 1:
            if pfd.switches[1].value == 1:
                #Chick went inside
                chicks_inside += 1
                print("CHICKEN WENT INSIDE: " + str(chicks_inside))
                if chicks_inside == chicks_amount and sun_down == True:
                    motor_down();
                break

    if event.pin_num == 1 and pifacedigital.switches[0].value == 0:
        while pifacedigital.switches[1].value == 1:
            if pifacedigital.switches[0].value == 1:
                #Chick went outside
                if chicks_inside > 0:
                    chicks_inside -= 1
                print("CHICKEN WENT OUTSIDE: " + str(chicks_inside))
                break
    
def set_Bool1_ON():
    global GATE_LED_BOOL1
    GATE_LED_BOOL1 = True
    
def set_Bool1_OFF():
    global GATE_LED_BOOL1
    GATE_LED_BOOL1 = False
    
def set_Bool2_ON():
    global GATE_LED_BOOL2
    GATE_LED_BOOL2 = True
    
def set_Bool2_OFF():
    global GATE_LED_BOOL2
    GATE_LED_BOOL2 = False
    

def run_general():
    Current_state = 0
    Previous_state = 0
    global TOTAL_CHICKS_INSIDE
    global gate_state
    global pot_level0
    global pot_level1
    while True:
        #print('BOOL1 = {}, BOOL2 = {}'.format(GATE_LED_BOOL1, GATE_LED_BOOL2))
        #Kip gaat mogelijk naar binnen
        if GATE_LED_BOOL1 == 1 and GATE_LED_BOOL2 == 0 and Previous_state == 0:
            #print("Check State IN")
            Previous_state = 11
        elif GATE_LED_BOOL1 == 1 and GATE_LED_BOOL2 == 1 and Previous_state == 11:
            Previous_state = 12
        elif GATE_LED_BOOL1 == 0 and GATE_LED_BOOL2 == 1 and Previous_state == 12:
            Previous_state = 13
        elif GATE_LED_BOOL1 == 0 and GATE_LED_BOOL2 == 0 and Previous_state == 13:
            #Kip naar binnen
            if TOTAL_CHICKS_INSIDE  < TOTAL_CHICKS_AMOUNT :
                TOTAL_CHICKS_INSIDE = TOTAL_CHICKS_INSIDE + 1
                print("CHICKEN WENT INSIDE: " + str(TOTAL_CHICKS_INSIDE))
            else:
                print("VOS VOS VOS VOS VOS VOSJE")
            Previous_state = 0
            
        #Kip gaat mogelijk naar buiten
        elif GATE_LED_BOOL1 == 0 and GATE_LED_BOOL2 == 1 and Previous_state == 0:
            #print("Check State OUT")
            Previous_state = 21
        elif GATE_LED_BOOL1 == 1 and GATE_LED_BOOL2 == 1 and Previous_state == 21:
            Previous_state = 22
        elif GATE_LED_BOOL1 == 1 and GATE_LED_BOOL2 == 1 and Previous_state == 22:
            Previous_state = 23
        elif GATE_LED_BOOL1 == 0 and GATE_LED_BOOL2 == 0 and Previous_state == 23:
            #Kip naar buiten
            if TOTAL_CHICKS_INSIDE != 0:
                TOTAL_CHICKS_INSIDE = TOTAL_CHICKS_INSIDE - 1
                print("CHICKEN WENT OUTSIDE: " + str(TOTAL_CHICKS_INSIDE))
            else:
                print("Huh?!? The coop should be empty already!")
            Previous_state = 0
            
        if TOTAL_CHICKS_INSIDE == TOTAL_CHICKS_AMOUNT and sun_down == True:
            gate_state = False
        if TOTAL_CHICKS_INSIDE == TOTAL_CHICKS_AMOUNT and sun_down == False:
            gate_state = True
            
        if pot_level0 < 512:
            set_Bool1_ON()
        elif pot_level0 >= 512:
            set_Bool1_OFF()   
        if pot_level1 < 512:
            set_Bool2_ON()
        elif pot_level1 >= 512:
            set_Bool2_OFF()
            

        check_sun = str(datetime.datetime.now().strftime("%H:%M"))
        if(check_sun == "20:00"):
            set_sun_time()

def run_spi():
    global pot_level0
    global pot_level1
    while True:
        pot_level0 = ReadChannel(INFRARED_LED_SPI0)
        pot_level1 = ReadChannel(INFRARED_LED_SPI1)
        pot_volts0 = ConvertVolts(pot_level0, 2)
        pot_volts1 = ConvertVolts(pot_level1, 2)
    
        # Print out results
        print("SPI Values: {} ({}V), {} ({}V)".format(pot_level0, pot_volts0, pot_level1, pot_volts1))
    
        # Wait before repeating loop
        time.sleep(READING_DELAY)

def run_flask_api():
    api.add_resource(Gate, '/toggle-gate/<string:gate_command>')
    api.add_resource(Total_Chicks_Inside, '/total-chicks-inside/')
    api.add_resource(Change_Chick_amount, '/change-count/<string:total_chicks>')
    while True:
        app.run(host='0.0.0.0')
        time.sleep(1)
        
def run_motor():
    #while pfd.input_pins[MOTOR_UP].value == 1:  
    pfd = pdio.PiFaceDigital()
    global gate_state
    while True:
        while gate_state == True:
            for num in range(0,25):
                pfd.output_pins[MOTOR_ENABLE].turn_off() #enable ON
                pfd.output_pins[MOTOR_STEER_1].turn_off()
                pfd.output_pins[MOTOR_STEER_2].turn_on()
                '''
            for num in range(0,5):
                pfd.output_pins[MOTOR_ENABLE].turn_on() #enable OFF
                pfd.output_pins[MOTOR_STEER_1].turn_on()
                pfd.output_pins[MOTOR_STEER_2].turn_on()
                '''
        while gate_state == False:
            pfd.output_pins[MOTOR_ENABLE].turn_on() #enable OFF
            pfd.output_pins[MOTOR_STEER_1].turn_on()
            pfd.output_pins[MOTOR_STEER_2].turn_on()

if __name__ == '__main__':
    try:
        t1 = thd.Thread(target = run_general)
        t2 = thd.Thread(target = run_spi)
        t3 = thd.Thread(target = run_flask_api)
        t4 = thd.Thread(target = run_motor)
        t1.setDaemon(True)
        t2.setDaemon(True)
        t3.setDaemon(True)
        t3.setDaemon(True)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        
        pdio.init()
        pfd = pdio.PiFaceDigital()
        listener = pdio.InputEventListener(chip=pfd)
        listener.register(0, pdio.IODIR_FALLING_EDGE, read_data)
        #listener.register(1, pdio.IODIR_FALLING_EDGE, motor_down)
        #listener.register(2, pdio.IODIR_FALLING_EDGE, motor_up)
        listener.register(1, pdio.IODIR_FALLING_EDGE, set_LED_bool1)
        listener.register(2, pdio.IODIR_FALLING_EDGE, set_LED_bool2)
        #listener.register(6, pdio.IODIR_ON, switch_pressed)
        #listener.register(7, pdio.IODIR_OFF, switch_unpressed)
        listener.activate()
        
        set_sun_time()
        if(sun_down == False):
            gate_state = True
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print('\nBye Bye Darling')
        listener.deactivate() 
        spi.close()
        sys.exit()
    