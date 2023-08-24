First run the pubkeygen.py script to generate the public key

Once the public key generated message is shown and the dsa_public_key.pem file is created in the folder you can run the A2P1.py script to generate scriptPubKey.txt and scriptSig.txt

Enter the number of public keys and the number of signatures required. Ensure that the number of signatures(M) is less than or equal to the number of public keys(N). if key pairs and signatures signed successfully a message is displayed on the terminal and the files scriptPubKey.txt and scriptSig.txt file can be seen in the folder.

Next we can the A2P2.py script to simulate the P2MS verification.
We enter the matching scriptPubKey and scriptSig file names pair for a successful simulation or you can enter a mismatched pair for a wrong key-sig simulation.
The script will find the first key-signature pair and once it has found the first pair, the subsequent pairs will all be correct. In the terminal the value 1 is pushed into the stack it means that all the number of key-sig pairs matches M. if the wrong key-sig pair is entered, it will push a 0 into the stack.

