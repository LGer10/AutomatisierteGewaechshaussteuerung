#!/usr/bin/python3

# automatisiertes gewächshaus | script - create database | version 0.1

# libraries
import mysql.connector

# mysql database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AGdb"
)

# mysql database cursor
cursor = db.cursor()

# create database
cursor.execute("CREATE DATABASE AGdb")

# mysql database cursor close
cursor.close()
