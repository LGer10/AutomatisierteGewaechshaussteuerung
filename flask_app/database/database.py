# automatisiertes gewächshaus | script - create database | version 0.1


#Library für MySQL Verbindung
import mysql.connector

#Übergabe der Credentials für den MySQL Server 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="AGdb"
)

#Cursor zum Ausführen von SQL Befehlen
mycursor = mydb.cursor()

#SQL Befehl
#Datenbank erstellen
mycursor.execute("CREATE DATABASE AGdb")
