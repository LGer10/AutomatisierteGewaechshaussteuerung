#!/usr/bin/bash

#command line statement to backup mysql database
mysqldump -u root -p'AGdb' AGdb > AGdb_backup.sql
