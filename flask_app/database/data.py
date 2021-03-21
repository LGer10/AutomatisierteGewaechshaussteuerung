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
cursor.execute('INSERT INTO programms (name) VALUES ("Testprogramm")')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ("Temperatur", "°C")')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ("Helligkeit", "Stunden")')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ("Luftfeuchtigkeit", "°C")')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ("Bodenfeuchtigkeit", "°C")')


cursor.execute('INSERT INTO programm_parameter(id_programm, id_parameter, value) VALUES ((select id from programms where name = "Testprogramm"), (select id from parameters where name = "Temperatur"), 25) '
cursor.execute('INSERT INTO programm_parameter(id_programm, id_parameter, value) VALUES ((select id from programms where name = "Testprogramm"), (select id from parameters where name = "Helligkeit"), 8) '
cursor.execute('INSERT INTO programm_parameter(id_programm, id_parameter, value) VALUES ((select id from programms where name = "Testprogramm"), (select id from parameters where name = "Luftfeuchtigkeit"), 60) '
cursor.execute('INSERT INTO programm_parameter(id_programm, id_parameter, value) VALUES ((select id from programms where name = "Testprogramm"), (select id from parameters where name = "Bodenfeuchtigkeit"), 50) '



db.commit()
cursor.close()
db.close()