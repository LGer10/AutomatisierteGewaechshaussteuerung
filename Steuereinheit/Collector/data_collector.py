#!/usr/bin/python3

# data collector script | Automatisiertes Gewächshaus | version 0.1

# Libraires
import mysql.connector
import sys
import requests
import time
import json
from datetime import datetime

# MySQL database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        database="AGdb",
        user="root",
        password="AGdb"
    )
# output if connection failed
except:
    print("Connection failed")
    sys.exit(0)

# MySQL database cursor
cursor = db.cursor(buffered=True)

# select ip-adress from all satellites
cursor.execute("SELECT ip_addr FROM satellites where id = 23")
satellite_ip = cursor.fetchall()

# colect data
def collector():
    # for-loop trough all satellites
    try:
        for satellite in satellite_ip[0]:
            # select current programm of satellite for later insert statement
            cursor.execute(
                'SELECT current_programm FROM satellites WHERE ip_addr = (%s)', [satellite])
            current_programm = cursor.fetchone()
            current_programm = current_programm[0]

            # request to REST-API
            # insert ip-address to url
            response = requests.get("http://" + satellite + ":8081/get_data")
            # respons as json file
            json_file = json.loads(response.text)

            # get parameters from json
            temperature = json_file["temperature"]
            brightness = json_file["brightness"]
            soil_humidity = json_file["soil_humidity"]
            air_humidity = json_file["air_humidity"]

            # convert brightness to hours
            # brightness treshhold is 200
            if brightness >= 200:
                brightness = 1/60
            # if brightness below treshhold insert 0 for brightness in database
            else:
                brightness = 0

            # ID satellite_programm for insert statement
            cursor.execute('''SELECT id from satellite_programm where id_satellite in 
            (select id from satellites where ip_addr = (%s) and current_programm = (%s))''', [satellite, current_programm])
            id_satellite_p = cursor.fetchone()
            id_satellite_programm = id_satellite_p[0]

            # insert parameters into table sensordata
            cursor.execute('''INSERT INTO sensordata 
            (id_satellite_programm, date, time, temperature, brightness, airhumidity, soilhumidity) 
            VALUES ((%s), current_date(), current_time(), (%s), (%s), (%s), (%s))''', [id_satellite_programm, temperature, brightness, air_humidity, soil_humidity])

            # commit insert
            db.commit()
    # exception if datacollection failed
    except:
        print('data-collection failed')
        time.sleep(5)


# call collector method
collector()
# close mysql cursor
cursor.close()
