#!/usr/bin/bash

#command line statement to restore mysql database
mysqldump -u root -p'AGdb' AGdb < AGdb_backup.sql
