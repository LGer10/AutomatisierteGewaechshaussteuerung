#!/usr/bin/bash

# automatisiertes gewächshaus | script - restore mysql database | version 0.1


echo enter file to restore

read file

#command line statement to restore mysql database
mysql -u root -p'AGdb' AGdb < /media/usbstick/$file

echo database recovered
