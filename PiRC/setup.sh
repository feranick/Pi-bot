#!/bin/bash

webfolder="/var/www/html/pirc"

chmod +x piRC.py
mkdir $webfolder

cp WebServer/* $webfolder
chmod 777 $webfolder/powerStatus.txt
chmod 777 $webfolder/steerStatus.txt

echo Done!
