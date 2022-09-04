import os
import re
import sys

from PIL import Image
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import logging

CHUNKSIZE = 32 * 1024


def create_key(inputValue):
    return SHA256.new(inputValue.encode(
        'utf-8')).digest()  # Create the Hash for the password, which is used for the encryption and decryption


def remove_file(file):
    try:
        os.remove(file)
    except Exception as e:
        logging.warning("Error in deleting file:" + str(e))


def encryptFile(key, filename, enctime):
    out_file = "/usr/share/cat_pictures_archive/encrypted_" + os.path.basename(filename)  # The file to write the encrypted data into
    file_size = str(os.path.getsize(filename)).zfill(16)  # get the filesize
    IV = Random.new().read(16)  # Initialisierungsvektor
    encryptor = AES.new(key, AES.MODE_CFB, IV)
    try:
        with open(filename, 'rb') as f_in:  # we need to have everything in binary
            with open(out_file, 'wb') as f_out:
                f_out.write(
                    file_size.encode(
                        'utf-8'))  # use utf-8 as standard in this script # write the size first in the file
                f_out.write(IV)  # has to be stored to decrypt the file
                while 1:
                    chunk = f_in.read(CHUNKSIZE)
                    if len(chunk) == 0:
                        logging.warning(
                            'encryption finished ' + enctime + ' ' + filename)
                        f_in.close()
                        f_out.close()
                        remove_file(filename)
                        break  # Break the while-loop, when document is fully read
                    if len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (
                                len(chunk) % 16))  # If the chunk is too short, we fill the empty space with binary whitespaces
                    f_out.write(encryptor.encrypt(chunk))
    except IOError:
        logging.warning(filename)


def dectyptFile(key, filename):
    out_file = filename + "_decrypted.jpg"
    try:
        with open(filename, 'rb') as f_in:  # the outputfile in binary
            filesize = int(f_in.read(16))  # read the filesize from the encrypted doc
            IV = f_in.read(16)  # read the IV from the encrypted doc
            decryptor = AES.new(key, AES.MODE_CFB, IV)  # initalize the decryptor similar to the encryptor
            with open(out_file, 'wb') as f_out:  # keep in mind -> everything in binary
                while 1:
                    chunk = f_in.read(CHUNKSIZE)
                    if len(chunk) == 0:  # break condition, when the chunk is empty
                        print('decryption done')
                        f_in.close()
                        f_out.close()
                        format = checkFormat(out_file)
                        print('checkFormat')
                        if format == '.jpg':
                            print('Decoded file into ' + format)
                            break
                        else:
                            print('decryption failed.')
                            remove_file(out_file)
                            break
                    f_out.write(decryptor.decrypt(chunk))  # decrypt the chunk
                    f_out.truncate(filesize)  # cut the added whitespaces in the end
    except Exception as e:
        logging.warning(filename)
        print(e)


def checkFormat(handle):
    print('l1')
    magic_numbers = {'jpg': bytes([0xFF, 0xD8, 0xFF, 0xE1]), }
    with open(handle, 'rb') as fd:
        file_head = fd.read(4)
    ext = 'jpg'
    if file_head.startswith(magic_numbers[ext]):
        return '.jpg'
    return None


def call(mode, enctime, file):
    switchmode = int(mode)

    pathToLogfile = "/usr/share/cat_pictures_archive"
    logfileExisist = os.path.exists(pathToLogfile + "/log.log")
    if not logfileExisist:
        logging.basicConfig(filename="/usr/share/cat_pictures_archive/log.log")

    if switchmode == 1:
        encryptFile(create_key(enctime), file, enctime)
    elif switchmode == 2:
        dectyptFile(create_key(enctime), file)
    else:
        return Exception('Mode 1: Encrypt, Mode 2: Decrypt')


def main(mode, password, file):
    call(mode, password, file)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
