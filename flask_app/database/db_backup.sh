#!/usr/bin/bash

# automatisiertes gewächshaus | script - backup mysql database | version 0.1

#command line statement to backup mysql database
mysqldump -u root -p'AGdb' AGdb > /media/usbstick/AGdb_backup-$(date +%Y%m%d).sql

#command line statement to delete backups older than 30 days
find /media/usbstick/* -mtime +30 -exec rm {} \;

