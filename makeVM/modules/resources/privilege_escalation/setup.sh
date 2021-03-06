# create user cat_miner
apt-get install useradd
/usr/sbin/useradd -m cat_miner -s /bin/bash

# set weak password for cat_miner
echo "cat_miner:cat" | chpasswd

#install pip
apt-get install -y python3-pip

#install crypto
pip install pycryptodome

# set SUID bit for base64
chmod u+s /usr/bin/base64

# install john the ripper
apt-get -y install john

# add john the ripper to path variable
ln -s /usr/sbin/john /usr/bin/john

# add unshadow to path variable
ln -s /usr/sbin/unshadow /usr/bin/unshadow

# create download folder for cronjob
mkdir /usr/share/downloaded_cat_pictures
chmod 744 /usr/share/downloaded_cat_pictures

# create archive folder for cat pictures
mkdir /usr/share/cat_pictures_archive
chmod 744 /usr/share/cat_pictures_archive/
mv cat1.jpg /usr/share/cat_pictures_archive/
mv cat2.jpg /usr/share/cat_pictures_archive/
mv cat3.jpg /usr/share/cat_pictures_archive/

# move server list to user cat_miner
mv ./cat_servers.txt /home/cat_miner/

# move cronjob to bin folder
mv ./cat_picture_maintenance.sh /usr/local/bin/


# crypt tool
mkdir /usr/local/bin/crypt
mv AESTool.py /usr/local/bin/crypt/
mv wrapperNew.py /usr/local/bin/crypt/
chmod 744 /usr/local/bin/crypt/AESTool.py
chmod 744 /usr/local/bin/crypt/wrapperNew.py


# create cronjob
echo '0-59 * * * * root sh /usr/local/bin/cat_picture_maintenance.sh' >> /etc/crontab
echo '0-59 * * * * root python3 /usr/local/bin/crypt/wrapperNew.py' >> /etc/crontab


# remove source folder
#rm -r ../privilege_escalation

