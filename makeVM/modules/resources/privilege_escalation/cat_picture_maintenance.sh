#/bin/bash

rm /usr/share/cat_pictures/*
cd /home/cat_miner/
wget -i ./cat_servers.txt -P /usr/share/cat_pictures
cd /usr/share/cat_pictures
tar czf /tmp/backup.tar.gz *

