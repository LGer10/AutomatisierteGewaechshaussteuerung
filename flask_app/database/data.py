#!/usr/bin/python3

# automatisiertes gewächshaus | script - data fro standar programms | version 0.1

# Libraries
import mysql.connector


# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    database="AGdb",
    user="root",
    password="AGdb"
)

# MySQL database cursor
cursor = db.cursor()

# create parameters
cursor.execute(
    'INSERT INTO parameters (name, unit) VALUES ("Temperatur", "°C")')
cursor.execute(
    'INSERT INTO parameters (name, unit) VALUES ("Helligkeit", "h")')
cursor.execute(
    'INSERT INTO parameters (name, unit) VALUES ("Luftfeuchtigkeit", "%")')
cursor.execute(
    'INSERT INTO parameters (name, unit) VALUES ("Bodenfeuchtigkeit", "%")')

# create programms
# chilis
cursor.execute('INSERT INTO programms (name) VALUES ("Chillis")')

# chilis-parameter
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Chillis"), (select id from parameters where name = "Temperatur"), 24)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Chillis"), (select id from parameters where name = "Helligkeit"), 8)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Chillis"), (select id from parameters where name = "Luftfeuchtigkeit"), 70)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Chillis"), (select id from parameters where name = "Bodenfeuchtigkeit"), 50)''')

# strawberries
cursor.execute('INSERT INTO programms (name) VALUES ("Erdbeeren")')

# strawberries-parameter
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Erdbeeren"), (select id from parameters where name = "Temperatur"), 20)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Erdbeeren"), (select id from parameters where name = "Helligkeit"), 10)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Erdbeeren"), (select id from parameters where name = "Luftfeuchtigkeit"), 70)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Erdbeeren"), (select id from parameters where name = "Bodenfeuchtigkeit"), 50)''')

# create satellite
# prototyp
cursor.execute(
    'INSERT INTO satellites (name, ip_addr) VALUES ("PrototypX", "192.168.1.100")')
cursor.execute('''INSERT INTO satellite_programm(id_programm, id_satellite) 
VALUES ((select id from programms where name = "Chillis"), (select id from satellites where name = "PrototypX"))''')
cursor.execute('''INSERT INTO satellite_programm(id_programm, id_satellite) 
VALUES ((select id from programms where name = "Erdbeeren"), (select id from satellites where name = "PrototypX"))''')

# commit inserts
db.commit()
# close cursor
cursor.close()
