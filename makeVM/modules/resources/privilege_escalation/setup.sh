# create user cat_miner
apt-get install useradd
/usr/sbin/useradd -m cat_miner

# set weak password for cat_miner
echo "cat_miner:cat" | chpasswd

# set SUID bit for base64
chmod u+s /usr/bin/base64

# install john the ripper
apt-get -y install john

# add john the ripper to path variable
ln -s /usr/sbin/john /usr/bin/john

# add unshadow to path variable
ln -s /usr/sbin/unshadow /usr/bin/unshadow

# create download folder for cronjob
mkdir /usr/share/cat_pictures
chmod 744 /usr/share/cat_pictures

# move server list to user cat_miner
mv ./cat_servers.txt /home/cat_miner/

# move cronjob to bin folder
mv ./cat_picture_maintenance.sh /usr/local/bin/

# create cronjob
echo '0-59 * * * * root sh /usr/local/bin/cat_picture_maintenance.sh' >> /etc/crontab

# remove source folder
rm -r ../privilege_escalation

