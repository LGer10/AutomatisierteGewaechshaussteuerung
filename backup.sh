#!/bin/bash

# variables
BACKUP_PATH="/media/usb"
BACKUP_NUMBER="2"
BACKUP_NAME="RaspberryPiBackup"
SERVICES_STOP="sudo systemctl stop mysql"
SERVICES_START="sudo systemctl start mysql"

# stop services (mysql)
${SERVICES_STOP}

# save zip-file of backup in path avriable
sudo dd if=/dev/mmcblk0 bs=1MB | gzip -c -9 > ${BACKUP_PATH}/${BACKUP_NAME}-$(date +%Y%m%d).img.gz

# start services (mysql)
${SERVICES_START}

# remove old backups
pushd ${BACKUP_PATH}; ls -tr ${BACKUP_PATH}/${BACKUP_NAME}* | head -n -${BACKUP_NUMBER} | xargs rm; popd
