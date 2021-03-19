# automatisiertes gewächshaus | script - create tables | version 0.1



#Library für MySQL Verbindung
import mysql.connector


#Übergabe der Credentials für die Datenbank 
db = mysql.connector.connect(
  host="localhost",
  database="AGdb",
  user="root",
  password="AGdb"
)

#Cursor zum Ausführen von SQL Befehlen
cursor = db.cursor()

#SQL Befehle
#Tabelle "satellites" erstellen
cursor.execute("CREATE TABLE satellites (id int NOT NULL AUTO_INCREMENT  PRIMARY KEY, name varchar(20), ip_addr varchar(36), current_programm int(2))")

#Tabelle "programms" erstellen
cursor.execute("CREATE TABLE programms (id int NOT NULL AUTO_INCREMENT PRIMARY KEY , name varchar(20), date_created timestamp)")

#Tabelle "satellite_programm" erstellen
cursor.execute('''CREATE TABLE satellite_programm (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, id_satellite int, id_programm int, FOREIGN KEY (id_satellite)
REFERENCES satellites(id), FOREIGN KEY (id_programm) REFERENCES programms(id))''')

#Tabelle "sensordata" erstellen
cursor.execute('''CREATE TABLE sensordata (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, id_satellite_programm int, date date, time time, temperature float(3),
brightness int(4), airhumidity float(3), soilhumidity float(3), FOREIGN KEY (id_satellite_programm) REFERENCES satellite_programm(id))''')

#Tabelle "parameters" erstellen
cursor.execute("CREATE TABLE parameters (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name varchar(20), unit varchar(5))")

#Tabelle "programm_parameter" erstellen
cursor.execute("CREATE TABLE programm_parameter (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, id_programm int, id_parameter int, value  varchar(4))")
