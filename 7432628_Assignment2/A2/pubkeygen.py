from Crypto.PublicKey import DSA
import binascii

#generate DSA key pair with 1024bit pub key
key = DSA.generate(1024)

#export the publikey in PEM format
pub_key_pem = key.publickey().export_key(format='PEM')

print("Public Key Generated")

#save pub key into a file
with open('dsa_public_key.pem','wb') as f:
	f.write(pub_key_pem)
