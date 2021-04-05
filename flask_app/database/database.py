#!/usr/bin/python3

# automatisiertes gewächshaus | script - create database | version 0.1

# Library für MySQL Verbindung
import mysql.connector

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AGdb"
)

# MySQL database cursor
cursor = db.cursor()

# create database
cursor.execute("CREATE DATABASE AGdb")

# MySQL database cursor close
cursor.close()
