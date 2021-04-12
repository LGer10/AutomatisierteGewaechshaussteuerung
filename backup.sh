#!/bin/bash

<<<<<<< HEAD
# 
BACKUP_PATH="/media/usb"
=======
# variables
BACKUP_PATH="/media/usbstick"
>>>>>>> 7267c8b414a6332890db92d038dbaf12f3918164
BACKUP_NUMBER="2"
BACKUP_NAME="RaspberryPiBackup"
SERVICES_STOP="sudo systemctl stop mysql"
SERVICES_START="sudo systemctl start mysql"

# stop services (mysql)
${SERVICES_STOP}

<<<<<<< HEAD
# Backup mit Hilfe von dd erstellen und im angegebenen Pfad speichern
dd if=/dev/mmcblk0 of=${BACKUP_PATH}/${BACKUP_NAME}-$(date +%Y%m%d).img bs=1MB

# Starte Dienste nach Backup
=======
# save zip-file of backup in path avriable
sudo dd if=/dev/mmcblk0 bs=1MB | gzip -c -9 > ${BACKUP_PATH}/${BACKUP_NAME}-$(date +%Y%m%d).img.gz
# start services (mysql)
>>>>>>> 7267c8b414a6332890db92d038dbaf12f3918164
${SERVICES_START}

# remove old backups
pushd ${BACKUP_PATH}; ls -tr ${BACKUP_PATH}/${BACKUP_NAME}* | head -n -${BACKUP_NUMBER} | xargs rm; popd
