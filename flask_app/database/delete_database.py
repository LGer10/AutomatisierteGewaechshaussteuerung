#!/usr/bin/python3

# automatisiertes gewächshaus | script - delete database for recovery | version 0.1

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

# statement to delet database for recovery
cursor.execute('DROP DATABASE AGdb')
# commit delete statement
db.commit()

cursor.close()

