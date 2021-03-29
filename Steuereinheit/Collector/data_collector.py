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

cursor = connection.cursor(buffered=True)

# Satelliten aus DB auslesen

cursor.execute("SELECT ip_addr FROM satellites where id = 3")
#cursor.execute("SELECT current_programm FROM satellites")


# Variablen in Array speichern

#satellit_array = cursor.fetchone()
satellite_list = cursor.fetchone()
# Verbindung schliessen

# cursor.close()


# Daten Collecten
def collector():
    try:
        for satellite in satellite_list:

    cursor = mysql.connection.cursor(buffered=True)
    # Aktuelle geladenes Programm abfragen
    cursor.excecute(
        'SELECT current_programm FROM satellites WHERE ip_addr = (%s)', [satellite])
    current_programm = cursor.fetchone()
    #current_programm = 1
    # REST-API anfragen

    response = requests.get("http://" + '%s' + ":8081/get_data", [satellite])
    json_file = json.loads(response.text)
    print(json_file)

    temperature = json_file["temperature"]
    brightness_hours = json_file["brightness_hours"]
    soil_humidity = json_file["Soil Humidity"]
    air_humidity = json_file["air_humidity"]

    cursor.execute('''SELECT id from satellite_programm where id_satellite in 
    (select id from satellites where ip_addr = (%s) and current_programm = (%s))''', [satellite, current_programm])

    id_satellite_programm = cursor.fetchone()

    cursor.execute('''INSERT INTO sensordata 
    (id_satellite_programm, date, time, temperature, brightness, airhumidity, soilhumidity) 
    VALUES (%s, current_date(), current_time(), %s, %s)''', [id_satellite_programm, temperature, brightness, air_humidity, soil_humidity])

    mysql.connection.commit()
    cursor.close()

    #cursor.execute("insert into sensordata (date, time, id_satellite_programm, temperature, airhumidity) values (%s, %s, '1', %s, %s), (current_date, current_time, temperature, air_humidity)")
    #cursor.execute("INSERT INTO sensordata (date, time, id_satellite_programm, temperature, airhumidity) VALUES (%s, %s, 1, %s, %s)", current_date, current_time, temperature, air_humidity)
    #cursor.execute("insert into sensordata (id_satellite_programm, temperature, airhumidity) values (1,23,56)")
    # cursor.fetchall()
    # cursor.commit()
    # break
    except:
        print('Error')
        print(satellite_array)
        time.sleep(5)


collector()
connection.close()
