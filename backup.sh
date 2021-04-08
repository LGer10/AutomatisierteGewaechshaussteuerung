#!/bin/bash

BACKUP_PFAD="/pfad/zum_backup_order"
BACKUP_ANZAHL="5"
BACKUP_NAME="RaspberryPiBackup"
DIENSTE_START_STOP="service mysql"

# Stoppe Dienste vor Backup
${DIENSTE_START_STOP} stop

# Backup mit Hilfe von dd erstellen und im angegebenen Pfad speichern
dd if=/dev/mmcblk0 of=${BACKUP_PFAD}/${BACKUP_NAME}-$(date +%Y%m%d-%H%M%S).img bs=1MB

# Starte Dienste nach Backup
${START_SERVICES} start

# Alte Sicherungen die nach X neuen Sicherungen entfernen
pushd ${BACKUP_PFAD}; ls -tr ${BACKUP_PFAD}/${BACKUP_NAME}* | head -n -${BACKUP_ANZAHL} | xargs rm; popd
