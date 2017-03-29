#!/usr/bin/python

import pymysql
import datetime
import time
import requests
import json


print("/----------------------------------------------------------\\")
print("|                        SELECT ALL                        |")
print("\----------------------------------------------------------/")

#On pi
#conn = pymysql.connect(host='localhost', user='root', passwd='root', db='ChickCounter')
#From laptop
conn = pymysql.connect(host='192.168.0.104', user='root', passwd='root', db='ChickCounter')

cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ChickCounter.chickens")
total_chicks = 0
for response in cur:
    total_chicks = total_chicks + 1
    print(response)

print("total_chicks: " + str(total_chicks))

cur.close()
#conn.close()


print("/----------------------------------------------------------\\")
print("|                          INSERT                          |")
print("\----------------------------------------------------------/")

#On pi
#conn = pymysql.connect(host='localhost', user='root', passwd='root', db='ChickCounter')
#From laptop
#conn = pymysql.connect(host='192.168.0.104', user='root', passwd='root', db='ChickCounter')

#chicks_inside = 2;
#ts = time.time()
#st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

#cur = conn.cursor()
#cur.execute("INSERT INTO ChickCounter.chickensInside (amount, time) VALUE ('"+ str(chicks_inside) + "','" + str(st) + "')")
#cur.close()

#print("Inserted number of chickens inside")

#conn.commit()
#conn.close()


print("/----------------------------------------------------------\\")
print("|                         API CALL                         |")
print("\----------------------------------------------------------/")


r = requests.get('https://api.darksky.net/forecast/a22f23bee010f3976f614a0460d1ccf6/50.87296604411913,4.697816732888441')
json_response = json.dumps(r.json(), ensure_ascii=False)
json_today = json.loads(json_response)['daily']['data'][0]
json_tomorrow = json.loads(json_response)['daily']['data'][1]

datetime.datetime.fromtimestamp(int("1284101485")).strftime('%Y-%m-%d %H:%M:%S')

#unix timestamp
sunrise_today = json_today['sunriseTime']
sunset_today = json_today['sunsetTime']
sunrise_tomorrow = json_tomorrow['sunriseTime']
sunset_tomorrow = json_tomorrow['sunsetTime']

#datetime
print ("sunrise today: " + str(datetime.datetime.fromtimestamp(int(sunrise_today)).strftime('%Y-%m-%d %H:%M:%S')))
print ("sunset today: " + str(datetime.datetime.fromtimestamp(int(sunset_today)).strftime('%Y-%m-%d %H:%M:%S')))
print ("sunrise tomorrow: " + str(datetime.datetime.fromtimestamp(int(sunrise_tomorrow)).strftime('%Y-%m-%d %H:%M:%S')))
print ("sunset tomorrow: " + str(datetime.datetime.fromtimestamp(int(sunset_tomorrow)).strftime('%Y-%m-%d %H:%M:%S')))


ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
print(st)



