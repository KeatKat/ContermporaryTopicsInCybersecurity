#!/usr/bin/env python3
import glob
import sys
import subprocess
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from base64 import b64decode
from Crypto.Util.Padding import unpad
import os

def change_file_extension(file_path, new_extension):
    file_name, old_extension = os.path.splitext(file_path)
    new_file_path = file_name + new_extension
    os.rename(file_path, new_file_path)
    return new_file_path

fixed_iv = b'\x00' * 16



try:
	file_in = open("Ck.bin", "rb") #open the Cipher key file
	private_key = RSA.import_key(open("private1.pem").read()) #get private key  from the private.pem file
	enc_key = file_in.read(private_key.size_in_bytes()) #get the encrypted symmetric key from Ck.bin
	cipher_rsa = PKCS1_OAEP.new(private_key) #version of RSA
	aes_key = cipher_rsa.decrypt(enc_key) #get symmetric key
	file_in.close()
	
	#read folder to get all txt files
	file_list = []
	for item in glob.glob("*.enc"):
	 new_extension = '.txt'
	 new_file_name = change_file_extension(item, new_extension)
	 file_list.append(new_file_name)


	 



	# Iterate over the encrypted files
	for item in file_list:
	 with open(item, 'r+b') as file_in:
	  #Read the ciphertext from the file
	  ciphertext = file_in.read()

	  #Create an AES cipher object with the key, CBC mode, and fixed IV
	  cipher = AES.new(aes_key, AES.MODE_CBC, fixed_iv)

	  #Decrypt and unpad the ciphertext
	  plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

	  #Seek to the beginning of the file and write the decrypted plaintext
	  file_in.seek(0)
	  file_in.write(plaintext)
	  file_in.truncate(len(plaintext))
	  file_in.close()

	  print('Decrypted', item)

except FileNotFoundError:
        print("Private key file not found. Please provide the correct path to the 'private.pem' or 'ck.bin' file. (line 23/24)")
except ValueError:
        print("Decryption failed. The private key might be incorrect or the files may have been tampered with.")
except Exception as e:
        print("An error occurred during decryption:", str(e))
			


