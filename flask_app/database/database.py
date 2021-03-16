import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="AGdb"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE AGdb")
