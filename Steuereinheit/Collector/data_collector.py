# data collector script | Automatisiertes Gewächshaus

# Klassen laden
import mysql.connector
import sys
import requests
import time
import json

# Variablen deklarieren

# Prüfen ob Datenbank verfügbar

try:
    connection = mysql.connector.connect(host = "127.0.0.1", user = "root", passwd = "huelsenschlaepper", db = "")
    print("Verbunden mit SQL Server")

except:
     print("Keine Verbindung zum Server")
     sys.exit(0)

cursor = connection.cursor()

# Satelliten laden

satellit_array = ("10.0.16.142", "10.0.16.143")

# Daten Collecten

try:
    for satellit in satellit_array:
        response = requests.get("http://" + satellit + ":8081/get_data")
        json_file = json.loads(response.text)

        temperature = json_file["temperature"]
        #brightness_hours = json_file["brightness_hours"]
        #soil_humidity = json_file["Soil Humidity"]
        air_humidity = json_file["air_humidity"]

        print(json_file)
        print(temperature)
        print(air_humidity)


        #cursor.execute("INSERT INTO  FROM inven WHERE titel LIKE %" ,(eingabe, ))
        
        
        
        break
except:
    time.sleep(5)








eingabe = input("Bitte hier ihre Suche eintragen: ")
cursor.execute("SELECT * FROM inven WHERE titel LIKE %" ,(eingabe, ))



result = cursor.fetchall()

cursor.close()
connection.close()

for r in result:
    print(r)




