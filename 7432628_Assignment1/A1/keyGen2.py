from Crypto.PublicKey import RSA

key = RSA.generate(2048) #generate public and private key pair

private_key = key.export_key() #export the private key
file_out = open("private2.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key() #export the public key
file_out = open("receiver2.pem", "wb")
file_out.write(public_key)
file_out.close()
