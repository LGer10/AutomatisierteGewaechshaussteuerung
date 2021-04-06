#!/usr/bin/python3

# automatisiertes gewächshaus | script - delete data older than 7 days | version 0.1

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

# statement to delet data from database older than 7 days
cursor.execute('DELETE FROM sensordata WHERE date < now() - interval 7 DAY')
# commit delete statement
db.commit()

cursor.close()

