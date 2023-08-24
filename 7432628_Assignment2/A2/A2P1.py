from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii




def DSAgen(n):
	file_path = 'dsa_public_key.pem'
	with open(file_path, 'r') as f:
		key_pem = f.read()
		
	param_key = DSA.import_key(key_pem)
	param = [param_key.p, param_key.q, param_key.g]
	
	key_pairs = []
	for x in range(1, n+1):
		
		#generate N pairs of DSA 1024 bit pubkey and private key
		key = DSA.generate(1024, domain= param)
		key_pairs.append(key)
		
	print (n, "Key Pairs Generated")
	return key_pairs


def signatures(message, m, key_pairs):

	signed_sigs = []
	for x in range(m):
		hash_obj = SHA256.new(message)
		signer = DSS.new(key_pairs[x], 'fips-186-3')
		signature = signer.sign(hash_obj)
		signed_sigs.append(signature)
	print(m, "Signatures Signed\n")
	return signed_sigs
			
def main():
	#msg to sign	
	message = b"CSCI301 Contemporary Topics in Security 2023"
	
	#making sure that M<=N before calling my functions to create the keys and sigs
	while(True):
		#taking user pubkey input and generating key pairs
		n = int(input("Enter number of public keys: "))
		m = int(input("Enter number of signatures: "))
		if(m<=n):
			break
		else:
			print("Value of M cannot be more than N\n")
	
	for num in range(1,4):
		key_pairs = DSAgen(n)
		signed_sigs = signatures(message,m,key_pairs)
		
		
		#creating scriptpubkey and scriptsig
		#hexlify the pubkey and signatures
		#{} are place holders for n and the public keys
		#convert the publickey from binary data into hexadecimal, add it into the placeholder
		scriptPubKey = "OP_{}\n{}\n".format(n, '\n'.join([binascii.hexlify(key_pair.publickey().export_key(format='DER')).decode() for key_pair in key_pairs]))
		
		scriptSig = "OP_{}\n{}\n".format(m, '\n'.join([binascii.hexlify(signature).decode() for signature in signed_sigs]))
		
		#adding the checkmultisig operator at the back
		scriptPubKey += "OP_CHECKMULTISIG"
		
		#saving scriptpubkey and scriptsig into files
		with open('scriptPubKey'+str(num)+'.txt', 'w') as f:
			f.write(scriptPubKey)
		
		with open('scriptSig'+str(num)+'.txt', 'w') as w:
			w.write(scriptSig)

	
	
	
if __name__ == "__main__":
	main()
