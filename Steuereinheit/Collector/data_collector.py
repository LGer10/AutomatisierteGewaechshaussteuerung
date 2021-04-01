# data collector script | Automatisiertes Gewächshaus | mit lärsu

# Klassen laden
import mysql.connector
import sys
import requests
import time
import json
from datetime import datetime
# Variablen deklarieren

# Prüfen ob Datenbank verfügbar

try:
    connection = mysql.connector.connect(
        host="localhost", user="root", passwd="AGdb", db="AGdb")
    #print("Verbunden mit SQL Server")

except:
    print("Keine Verbindung zum Server")
    sys.exit(0)

# Satelliten aus DB auslesen
cursor = connection.cursor(buffered=True)

cursor.execute("SELECT ip_addr FROM satellites where id = 7")

# Variablen in Array speichern

#satellit_array = cursor.fetchone()
satellite_ip = cursor.fetchall()
satellite_ip_array = []
for index in range(len(satellite_ip)):
    satellite_ip_array.append(satellite_ip[index][0])


# Daten Collecten
def collector():

    for satellite in satellite_ip_array:

        print(satellite)
        # Aktuelle geladenes Programm abfragen
        cursor.execute(
            'SELECT current_programm FROM satellites WHERE ip_addr = (%s)', [satellite])
        current_programm = cursor.fetchone()
        current_programm = current_programm[0]

    # REST-API anfragen
        print(current_programm)
        response = requests.get(
            "http://" + satellite + ":8081/get_data")
        json_file = json.loads(response.text)

        temperature = json_file["temperature"]
        brightness = json_file["brightness"]
        soil_humidity = json_file["soil_humidity"]
        air_humidity = json_file["air_humidity"]

        print(temperature)

        cursor.execute('''SELECT id from satellite_programm where id_satellite in 
        (select id from satellites where ip_addr = (%s) and current_programm = (%s))''', [satellite, current_programm])

        id_satellite_programm = cursor.fetchone()

        cursor.execute('''INSERT INTO sensordata 
        (id_satellite_programm, date, time, temperature, brightness, airhumidity, soilhumidity) 
        VALUES ((%s), current_date(), current_time(), (%s), (%s), (%s), (%s))''', [id_satellite_programm, temperature, brightness, air_humidity, soil_humidity])

        connection.commit()
        cursor.close()

    #cursor.execute("insert into sensordata (date, time, id_satellite_programm, temperature, airhumidity) values (%s, %s, '1', %s, %s), (current_date, current_time, temperature, air_humidity)")
    #cursor.execute("INSERT INTO sensordata (date, time, id_satellite_programm, temperature, airhumidity) VALUES (%s, %s, 1, %s, %s)", current_date, current_time, temperature, air_humidity)
    #cursor.execute("insert into sensordata (id_satellite_programm, temperature, airhumidity) values (1,23,56)")
    # cursor.fetchall()
    # cursor.commit()
    # break
    # except Exception as e:
     #   print(e)
      #  print('Error')
       # print(satellite_ip_array)
        # time.sleep(5)


collector()
connection.close()
