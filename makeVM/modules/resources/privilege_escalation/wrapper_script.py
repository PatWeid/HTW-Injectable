import os
import random
import logging
import datetime

from AESTool import call

path = '/usr/share/cat_pictures_archive'


def selectfile(pathToFolder):
    n = 1
    random.seed()
    for root, dir, files in os.walk(pathToFolder):
        for name in files:
            n += 1
            if random.uniform(0, n) < 1:
                selected = os.path.join(root, name)
                logging.info('Enrypted: ' + str(selected))
                return selected


def encryptSelectedFile(file):
    enctime = datetime.datetime.now().replace(microsecond=0).isoformat()
    logging.warning('logging done at: ' + enctime)
    call(1, enctime, path)


def main():
    logging.basicConfig(filename="logging.log")
    encryptSelectedFile(selectfile(path))
    #encryptSelectedFile(path)


if __name__ == '__main__':
    main()
