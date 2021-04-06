#!/usr/bin/python3

# automatisiertes gewächshaus | script - create tables | version 0.1

# libraries
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

# create tables
# satellites
cursor.execute("CREATE TABLE satellites (id int NOT NULL AUTO_INCREMENT  PRIMARY KEY, name varchar(30), ip_addr varchar(36), current_programm int(2))")

# programms
cursor.execute("CREATE TABLE programms (id int NOT NULL AUTO_INCREMENT PRIMARY KEY , name varchar(30), date_created timestamp)")

# satellite_programm
cursor.execute('''CREATE TABLE satellite_programm (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, id_satellite int, id_programm int, FOREIGN KEY (id_satellite)
REFERENCES satellites(id), FOREIGN KEY (id_programm) REFERENCES programms(id))''')

# sensordata
cursor.execute('''CREATE TABLE sensordata (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, id_satellite_programm int, date date, time time, temperature float(4),
brightness float(4), airhumidity float(4), soilhumidity float(4), FOREIGN KEY (id_satellite_programm) REFERENCES satellite_programm(id))''')

# parameters
cursor.execute("CREATE TABLE parameters (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name varchar(30), unit varchar(10))")

# programm_parameter
cursor.execute("CREATE TABLE programm_parameter (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, id_programm int, id_parameter int, value  varchar(4))")

# users
cursor.execute("CREATE TABLE users (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name varchar(30), password varchar(20), email varchar(30), date_created timestamp)")

# mysql database cursor close
cursor.close()
