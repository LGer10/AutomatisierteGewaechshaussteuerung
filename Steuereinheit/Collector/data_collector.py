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
    connection = mysql.connector.connect(host = "127.0.0.1", user = "root", passwd = "AGdb", db = "AGdb")
    #print("Verbunden mit SQL Server")

except:
     print("Keine Verbindung zum Server")
     sys.exit(0)

#cursor = connection.cursor(buffered=True)

# Satelliten aus DB auslesen

#cursor.execute("SELECT ip_addr FROM satellites")
#cursor.execute("SELECT current_programm FROM satellites")



# Variablen in Array speichern

#satellit_array = cursor.fetchone()
satellit_array = ['192.168.1.16', '192.168.1.16']
# Verbindung schliessen

#cursor.close()


# Daten Collecten
def collector():
    try:
        for satellit in satellit_array:

            cursor = mysql.connection.cursor(buffered=True)

            #Aktuelle geladenes Programm abfragen
            #cursor.excecute('SELECT current_programm FROM satellites WHERE ip_addr = (%s)', satellite)
            #current_programm = cursor.fetchone()
            current_programm = 1
            # REST-API anfragen

            response = requests.get("http://" + satellit + ":8081/get_data")
            json_file = json.loads(response.text)
            print(json_file)


            temperature = json_file["temperature"]
            #brightness_hours = json_file["brightness_hours"]
           # soil_humidity = json_file["Soil Humidity"]
            air_humidity = json_file["air_humidity"]


            cursor.execute('''SELECT id from satellite_programm where id_satellite in 
            (select id from satellites where ip_addr = (%S) and current_programm = (%S))''', [satellit, current_programm])

            id_satellite_programm = cursor.fetchone()

            cursor.execute('''INSERT INTO sensordata 
            (id_satellite_programm, date, time, temperature, airhumidity) 
            VALUES (%s, current_date(), current_time(), %s, %s)''', [id_satellite_programm, temperature, air_humidity])

            mysql.connection.commit()
            cursor.close()

            #cursor.execute("insert into sensordata (date, time, id_satellite_programm, temperature, airhumidity) values (%s, %s, '1', %s, %s), (current_date, current_time, temperature, air_humidity)")
            #cursor.execute("INSERT INTO sensordata (date, time, id_satellite_programm, temperature, airhumidity) VALUES (%s, %s, 1, %s, %s)", current_date, current_time, temperature, air_humidity)
            #cursor.execute("insert into sensordata (id_satellite_programm, temperature, airhumidity) values (1,23,56)")
            #cursor.fetchall()
            #cursor.commit()
            #break
    except:
        print('Error')
        time.sleep(5)

collector()
connection.close()