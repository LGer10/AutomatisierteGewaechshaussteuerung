# automatisiertes gewächshaus | script - data fro standar programms | version 0.1

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
#Programm1
cursor.execute('INSERT INTO programms (name) VALUES ("Testprogramm")')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ("Temperatur", "°C")')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ("Helligkeit", "h")')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ("Luftfeuchtigkeit", "°C")')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ("Bodenfeuchtigkeit", "°C")')

#Parameter
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Testprogramm"), (select id from parameters where name = "Temperatur"), 25)''') 
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Testprogramm"), (select id from parameters where name = "Helligkeit"), 8)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Testprogramm"), (select id from parameters where name = "Luftfeuchtigkeit"), 60)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Testprogramm"), (select id from parameters where name = "Bodenfeuchtigkeit"), 50)''')

#Programm2
cursor.execute('INSERT INTO programms (name) VALUES ("Testprogramm1")')

cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Testprogramm1"), (select id from parameters where name = "Temperatur"), 20)''') 
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Testprogramm1"), (select id from parameters where name = "Helligkeit"), 6)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Testprogramm1"), (select id from parameters where name = "Luftfeuchtigkeit"), 50)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Testprogramm1"), (select id from parameters where name = "Bodenfeuchtigkeit"), 40)''')

cursor.execute('INSERT INTO satellites (name, ip_addr) VALUES ("Testsatellit", "192.168.1.100")')
cursor.execute('''INSERT INTO satellite_programm(id_satellite, id_programm) 
VALUES ((select id from programms where name = "Testprogramm"), (select id from satellites where name = "Testsatellit"))''')
cursor.execute('''INSERT INTO satellite_programm(id_satellite, id_programm) 
VALUES ((select id from programms where name = "Testprogramm1"), (select id from satellites where name = "Testsatellit"))''') 

cursor.execute('''insert into sensordata (id_satellite_programm, temperature, brightness, airhumidity, soilhumidity, date, time) 
VALUES (1, 25, 8, 60, 50, cur_date(), cur_time())''')
cursor.execute('''insert into sensordata (id_satellite_programm, temperature, brightness, airhumidity, soilhumidity, date, time) 
VALUES (1, 30, 5, 50, 20, cur_date() - 1, cur_time())''')
cursor.execute('''insert into sensordata (id_satellite_programm, temperature, brightness, airhumidity, soilhumidity, date, time) 
VALUES (1, 20, 6, 60, 40, cur_date() - 2, cur_time())''')
cursor.execute('''insert into sensordata (id_satellite_programm, temperature, brightness, airhumidity, soilhumidity, date, time) 
VALUES (1, 10, 8, 40, 60, cur_date()- 3, cur_time())''')
cursor.execute('''insert into sensordata (id_satellite_programm, temperature, brightness, airhumidity, soilhumidity, date, time) 
VALUES (1, 20, 10, 80, 70, cur_date() -4, cur_time())''')

db.commit()
cursor.close()
db.close()