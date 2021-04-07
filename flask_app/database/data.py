#!/usr/bin/python3

# automatisiertes gewächshaus | script - data for standard programms | version 0.1

# Libraries
import mysql.connector


# mysql database connection
db = mysql.connector.connect(
    host="localhost",
    database="AGdb",
    user="root",
    password="AGdb"
)

# mysql database cursor
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

# strawberries
cursor.execute('INSERT INTO programms (name) VALUES ("Erdbeeren")')

# insert parameters
# chilis-parameter
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Chillis"), (select id from parameters where name = "Temperatur"), 24)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Chillis"), (select id from parameters where name = "Helligkeit"), 8)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Chillis"), (select id from parameters where name = "Luftfeuchtigkeit"), 70)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Chillis"), (select id from parameters where name = "Bodenfeuchtigkeit"), 50)''')

# strawberries-parameter
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Erdbeeren"), (select id from parameters where name = "Temperatur"), 20)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Erdbeeren"), (select id from parameters where name = "Helligkeit"), 10)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Erdbeeren"), (select id from parameters where name = "Luftfeuchtigkeit"), 70)''')
cursor.execute('''INSERT INTO programm_parameter(id_programm, id_parameter, value) 
VALUES ((select id from programms where name = "Erdbeeren"), (select id from parameters where name = "Bodenfeuchtigkeit"), 50)''')

# commit inserts
db.commit()
# close cursor
cursor.close()
