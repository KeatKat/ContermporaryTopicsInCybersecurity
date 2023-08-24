from Crypto.Signature import DSS
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA256
import binascii


def verify(overallStack):

	#pop N
	N = overallStack.pop()
	public_keys = []
	for x in range(N):
		public_keys.append(overallStack.pop())
		
	#pop M number of sigs that need to be verifies
	M = overallStack.pop()
	sigs = []
	for x in range(M):
		sigs.append(overallStack.pop())
	
	
	#verification
	message = b"CSCI301 Contemporary Topics in Security 2023"
	msg_hash = SHA256.new(message)
	
	#check first signature with all the public keys and break the for loop once the keypair is a match
	#save the current index of the correct key pair and continue from there
	cur_index = 0
	true_checker = []
	for pub_key_der in range(N):
		pub_key = DSA.import_key(public_keys[pub_key_der])
		verifier = DSS.new(pub_key, 'fips-186-3')
		
		try:
			verifier.verify(msg_hash,sigs[0])
			true_checker.append(True)
			if(pub_key_der != N-1):
				cur_index = pub_key_der
			print("Key-Sig pair 1 found")
			break
			
		except ValueError:
			print("Wrong Match")
	
	#for the signatures after the first, it should be paired up nicely, unless the correct signature pair was the last key, if so, set the current index back to 0 and the pairs should match up.
	if(len(true_checker) == 1):
		for sig in sigs[1:M]:
			cur_index+=1
			pub_key = DSA.import_key(public_keys[cur_index])
			verifier = DSS.new(pub_key, 'fips-186-3')
			try:
				verifier.verify(msg_hash,sig)
				true_checker.append(True)
				print("Key-Sig pair {} found".format(len(true_checker)))
				
			except ValueError:
				print(ValueError)		
		print("{}/{} Key-Sig Pairs found".format(len(true_checker),M))
		overallStack.append(1)
		print("overallStack : ", overallStack)
	else:
		print("{}/{} Key-Sig Pairs found".format(len(true_checker),M))
		print("Invalid number of Key-Sig pairs")
		overallStack.append(0)
		print("overallStack : ", overallStack) 
				
		
		
	

			
	
def createStack(public_keys, signatures):
	
	overallStack = []
	#split the operators and the pubkeys/sigs with \n as the delimiter
	pubkey_lines = public_keys.split('\n')
	sig_lines = signatures.split('\n')
	#get the number of pkeys and sigs
	n = int(pubkey_lines[0].split('_')[1])
	m = int(sig_lines[0].split('_')[1])
	
	#form the stack, if it reaches check multisig, do verification
	for sigs in sig_lines[1:m+1]:
		overallStack.append(binascii.unhexlify(sigs))
	
	overallStack.append(m)
	
	for pklines in pubkey_lines[1:n+2]:
		if(pklines == "OP_CHECKMULTISIG"):
			overallStack.append(n)
			verify(overallStack)
		else:
			overallStack.append(binascii.unhexlify(pklines))
		
	

def main():
	#open the generated script files
	#.strip() to remove any whitespaces in the file
	
	scriptPK = input("Enter pub key script filename: ")
	scriptSG = input("Enter sig script filename: ")
	with open(scriptPK, 'r') as pub_keys:
		scriptPubKey = pub_keys.read().strip()
	
	with open(scriptSG, 'r') as sigs:
		scriptSig = sigs.read().strip()
	
	createStack(scriptPubKey,scriptSig)
	
	
	
	
		
	
		
	
		
	



if __name__ == "__main__":
	main()
