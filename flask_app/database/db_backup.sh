#!/usr/bin/bash

#command line statement to backup mysql database
mysqldump -u root -p'AGdb' AGdb > AGdb_backup.sql

#command line statement to delete backups older than 30 days
find /home/pi/projects/automatisiertes_gewaechshaus/flask_app/database/backups/* -mtime +30 -exec rm {} \;

