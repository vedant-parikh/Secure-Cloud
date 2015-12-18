__author__ = 'Vedant and Kenil'

import Encrypt_and_Upload_to_Dropbox
import Decrypt_and_Download_from_Dropbox


print "Select from the choices"
print "1. Encrypt and upload a file:"
print "2. Decrypt and download a file:"
input_value = raw_input()
if input_value == '1':
    Encrypt_and_Upload_to_Dropbox.encryptFunction()
elif input_value == '2':
    Decrypt_and_Download_from_Dropbox.decryptFunction()
