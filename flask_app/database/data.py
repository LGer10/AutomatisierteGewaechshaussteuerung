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
cursor.execute('INSERT INTO programms (name, date_created) VALUES ('Testprogramm', current_timestamp())')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ('Temperatur', '°C')')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ('Helligkeit', 'Stunden')')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ('Luftfeuchtigkeit', '°C')')
cursor.execute('INSERT INTO parameters (name, unit) VALUES ('Bodenfeuchtigkeit', '°C')')

cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter)
SELECT pr.id = pa.id
FROM programms pr
JOIN parameters pa
ON programm_parameter.id_programm = pr.id where pa.name = 'Temperatur'
JOIN programms_parameter.id_parameter = pa.id
  ''')

cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter)
SELECT pr.id = pa.id
FROM programms pr
JOIN parameters pa
ON programm_parameter.id_programm = pr.id where pa.name = 'Helligkeit'
JOIN programms_parameter.id_parameter = pa.id
  ''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter)
SELECT pr.id = pa.id
FROM programms pr
JOIN parameters pa
ON programm_parameter.id_programm = pr.id where pa.name = 'Luftfeuchtigkeit'
JOIN programms_parameter.id_parameter = pa.id
  ''')
  cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter)
SELECT pr.id = pa.id
FROM programms pr
JOIN parameters pa
ON programm_parameter.id_programm = pr.id where pa.name = 'Bodenfeuchtigkeit'
JOIN programms_parameter.id_parameter = pa.id
  ''')

cursor.execute('update table programm_parameter set value = 25 where id_parameter in (select id from parameters where name ='Temperature') ')
cursor.execute('update table programm_parameter set value = 8 where id_parameter in (select id from parameters where name ='Helligkeit') ')
cursor.execute('update table programm_parameter set value = 60 where id_parameter in (select id from parameters where name ='Luftfeuchtigkeit') ')
cursor.execute('update table programm_parameter set value = 50 where id_parameter in (select id from parameters where name ='Bodenfeuchtigkeit') ')

db.commit()
cursor.close()
db.close()