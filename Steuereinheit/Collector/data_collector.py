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
    connection = mysql.connector.connect(host = "127.0.0.1", user = "root", passwd = "sml12345", db = "AGdb")
    #print("Verbunden mit SQL Server")

except:
     print("Keine Verbindung zum Server")
     sys.exit(0)

cursor = connection.cursor(buffered=True)

# Satelliten aus DB auslesen

cursor.execute("SELECT ip_addr FROM satellites")

# Variablen in Array speichern

satellit_array = cursor.fetchone()

# Verbindung schliessen

cursor.close()


# Daten Collecten
def collector():
    try:
        for satellit in satellit_array:

            # REST-API anfragen

            response = requests.get("http://" + satellit + ":8081/get_data")
            json_file = json.loads(response.text)
            #print(json_file)

            current_date = datetime.date(datetime.now())
            current_time = datetime.time(datetime.now())

            temperature = json_file["temperature"]
            #brightness_hours = json_file["brightness_hours"]
            #soil_humidity = json_file["Soil Humidity"]
            air_humidity = json_file["air_humidity"]


            cursor = connection.cursor(buffered=True)

            add_data = ("INSERT INTO sensordata"
                       "(date, time, id_satellite_programm, temperature, airhumidity) "
                       "VALUES (%s, %s, %s, %s, %s)")

            data_data = (current_date, current_time, '1', temperature, air_humidity)
            cursor.execute(add_data, data_data)

            #cursor.fetchall()

            connection.commit()
            cursor.close()

            #cursor.execute("insert into sensordata (date, time, id_satellite_programm, temperature, airhumidity) values (%s, %s, '1', %s, %s), (current_date, current_time, temperature, air_humidity)")
            #cursor.execute("INSERT INTO sensordata (date, time, id_satellite_programm, temperature, airhumidity) VALUES (%s, %s, 1, %s, %s)", current_date, current_time, temperature, air_humidity)
            #cursor.execute("insert into sensordata (id_satellite_programm, temperature, airhumidity) values (1,23,56)")
            #cursor.fetchall()
            #cursor.commit()
            #break
    except:
        time.sleep(5)

collector()
connection.close()