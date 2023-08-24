from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from queue import Queue
import json
import hashlib
import time
import threading
import os


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-91f28bf5-2023-4616-a8fe-6aa37872db0a'
pnconfig.publish_key = 'pub-c-7e999981-9223-421d-bacc-41f79dde5c25'
pnconfig.user_id = "KeatApp"
pubnub = PubNub(pnconfig)

#global var
blknum = None
stop_mining_event = threading.Event()

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):

    def __init__(self):
    	#so that i can store the message as an instance variable to be accessed
        super().__init__()
        self.received_message = None

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel('Channel-Barcelona').message('Hello world!').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        self.received_message = message.message
	


def genesis():
	with open("0.json","r") as file_in:
		gen_block = json.load(file_in)
		file_in.close()
	transactions = gen_block["Transaction"]
	return transactions


def mining(transactions):
	global blknum,stop_mining_event
	blknum=0
	for i in transactions:
		time.sleep(1.5)
		blknum +=1
		fr = open(str(blknum-1) + ".json","r")
		preblk = fr.read() #read hash from previous blk
		fr.close()
		prehash = hashlib.sha256(preblk.encode()).hexdigest() #hash of previous blk
		
		#make sure meets criteria before adding into the block chain
		nonce = 0
		cond = True
		success = False
		print(f"Finding hash for block {blknum}\n")
		while(cond):
			#break the block finding if bob already found that block
			if stop_mining_event.is_set():
				print(f"Skipping {blknum} as Bob has already found {blknum}")
				stop_mining_event.clear()
				cond = False
			
			#genesis blk contains empty transaction
			tx = json.dumps({'Block number': blknum, 'Hash': prehash, 'Nonce':nonce, 'Transaction': i},sort_keys=True, indent=4,separators=(',', ': '))
			hashcheck = hashlib.sha256(tx.encode()).hexdigest()
			if int(hashcheck,16) < 2**236:
				cond = False
				success = True
			nonce +=1
		#only if it reaches here and stop_minin_event is not set (meaning bob didnt find the block) then send the message to bob
		if success == True:
			print(f"Found hash for block {blknum}")
			pubnub.publish().channel('Channel-Bob').message(tx).pn_async(my_publish_callback)
			if not os.path.exists(str(blknum) + ".json"):
				fw = open(str(blknum) + ".json", "w+")
				fw.write(tx)
				fw.close()
			else:
				print(f"Bob mined {blknum} first")
				
			#introduce a delay because if the nonce is too small and the delivery is "instant" it will mess with the order of the checking and skipping


def verify(received_message):
	
	#get blknum for crr blk
	block = json.loads(received_message)
	blknum = block["Block number"]
	fr = open(str(blknum-1) + ".json","r")
	preblk = fr.read() #read hash from previous blk
	fr.close()
	prehash = hashlib.sha256(preblk.encode()).hexdigest() #hash of previous blk
	
	
	fr2 = open(str(blknum) + ".json", "r")
	crrblk = fr2.read()
	fr2.close()
	currhash = json.loads(crrblk)['Hash']
	
	
	if int(prehash,16) == int(currhash,16):
		return True
	else:
		return False
		
def message_handler():
	global stop_mining_event
	while True:
		if my_subscribe_callback.received_message is not None:
			received_message = my_subscribe_callback.received_message
			print(received_message)
			my_subscribe_callback.received_message = None
			block_check = verify(received_message)
			print(block_check)
			block_num = json.loads(received_message)['Block number']
			#check if the file already exists (in the case of simultaneous finding)
			if block_check == True and os.path.exists(str(block_num) + '.json'):
				#set the event so that the while loop breaks
				stop_mining_event.set()
				
			
			
		else:
			time.sleep(1)
				
			
			
		


	
if __name__ == "__main__":
	
	#connection
	my_subscribe_callback = MySubscribeCallback()
	pubnub.add_listener(my_subscribe_callback)
	pubnub.subscribe().channels('Channel-Alice').execute()
	
	
	#threading
	transactions = genesis()

	mining_thread = threading.Thread(target=mining, args=(transactions,))
	mining_thread.start()
	
	message_handling_thread = threading.Thread(target=message_handler)
	message_handling_thread.start()
	
	mining_thread.join()
	message_handling_thread.join()
	
	#now i need to take the block received and stop mining that
	

	
	


