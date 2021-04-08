#!/bin/bash

# 
BACKUP_PATH="/media/usbstick"
BACKUP_NUMBER="2"
BACKUP_NAME="RaspberryPiBackup"
SERVICES_STOP="systemctl stop mysql"
SERVICES_START="systemctl start mysql"

# Stoppe Dienste vor Backup
${SERVICES_STOP}

# Backup mit Hilfe von dd erstellen und im angegebenen Pfad speichern
dd if=/dev/mmcblk0 of=${BACKUP_PFAD}/${BACKUP_NAME}-$(date +%Y%m%d).img bs=1MB

# Starte Dienste nach Backup
${SERVICES_START}

# Alte Sicherungen die nach X neuen Sicherungen entfernen
pushd ${BACKUP_PATH}; ls -tr ${BACKUP_PATH}/${BACKUP_NAME}* | head -n -${BACKUP_NUMBER} | xargs rm; popd
