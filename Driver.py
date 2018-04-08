import User
import Group
import Activity
import DataEntry
import DataType
import Privs


#reference: http://ecomunsing.com/build-your-own-blockchain

import hashlib, json, sys, random, time

random.seed(0)

def hashMe(msg=""):
    # For convenience, this is a helper function that wraps our hashing algorithm
    if type(msg)!=str:
        msg = json.dumps(msg,sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability!
        
    if sys.version_info.major == 2:
        return unicode(hashlib.sha256(msg).hexdigest(),'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()
		
def sendAlert(user, entry):
	print("ALERT: USER", user, "IS ACCESSING", entry, "WAY TOO FUCKING MUCH")

def isValidTxn(txn, state):

	txnUser = txn[0]
	txnData = txn[2]
	
	if txnUser.isSuspended != 0:
		return False
	if txnData.DataType in txnUser.SuspendedDataTypes:
		return False
	
	if txn[3] == "r":
		for i in txnUser.userActivity.dataTypeReadsPerHour:
			if i[0] is txnData.DataType:
			
				if state[txnUser.name][0] > (1.4 * i[1]):
					sendAlert(txnUser.name, txnData.name)
				if state[txnUser.name][0] > (1.6 * i[1]):
					txnUser.isSuspended = pow(5, txnData.sen)
					return False
					
				return True
			
			else:
				return False
				
	else:
		for i in txnUser.userActivity.dataTypeWritesPerHour:
			if i[0] is txnData.DataType:
			
				if state[txnUser.name][1] > (1.4 * i[1]):
					sendAlert(txnUser.name, txnData.name)
				if state[txnUser.name][1] > (1.6 * i[1]):
					txnUser.isSuspended = pow(5, txnData.sen)
					return False
					
				return True
			
			else:
				return False
				
	
	
	return False
	
def makeBlock(txns,chain):

	if len(chain) == 0:
		genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':txns}
		for item in txns:
			item[0] = item[0].name
			item[2] = item[2].name
		genesisHash = hashMe( genesisBlockContents )
		genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
		genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)
		return genesisBlock

	parentBlock = chain[-1]
	parentHash  = parentBlock[u'hash']
	blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
	txnCount    = len(txns)
	blockContents = {u'blockNumber':blockNumber,u'parentHash':parentHash, u'txnCount':len(txns),'txns':txns}
	for item in txns:
		item[0] = item[0].name
		item[2] = item[2].name
	blockHash = hashMe( blockContents )
	block = {u'hash':blockHash,u'contents':blockContents}
    
	return block
	
def updateState(txn, state):
	state = state.copy()
	if txn[0].name in state.keys():
		if txn[3] == "r":
			state[txn[0].name][0] += 1
		else:
			state[txn[0].name][1] += 1
	else:
		if txn[3] == "r":
			state[txn[0].name] = [1,0]
		else:
			state[txn[0].name] = [0,1]
	return state

Bob = User.User()
Bob.ID = 123


personalRecords = DataType.DataTypes()
personalRecords.name = "Personal Records"
personalRecords.sensitivity = 7
personalRecords.frequencyOfAccess = 10
personalRecords.reviewTime = 4000
personalRecords.Immutability = 8

AlicePrivs = Privs.Priviledge()
AlicePrivs.read = True
AlicePrivs.TypeOfData = "Personal Records"

AliceAct = Activity.Activity()
AliceAct.sensitivityAccesses = 10
AliceAct.accessesPerHour = 10
AliceAct.readsPerHour = 10
AliceAct.writesPerHour = 10
AliceAct.changeSecAttributes = 10

AliceAct.dataTypeAccessesPerHour.append([personalRecords, 10])
AliceAct.dataTypeReadsPerHour.append([personalRecords, 10])
AliceAct.dataTypeWritesPerHour.append([personalRecords, 10])
AliceAct.dataTypeSecAttributesPerHour.append([personalRecords, 10])

Alice = User.User()
Alice.email = "Someemail@domain.com"
Alice.phoneNumber = "1111111111"
Alice.name = "Alice"
Alice.privList.append(AlicePrivs)
Alice.ID = 12
Alice.managerID = 123
Alice.userActivity =  AliceAct
Alice.dataTypeAccess.append(personalRecords)


record = DataEntry.DataEntry()
record.sen = 3
record.imm = 9
record.name = "record"
record.integrity = 9
record.protocol = None
record.ReviewTime = 100
record.freqAccess = 9
record.DataType = personalRecords
record.ownerList.append(Bob)
record.managerList.append(Alice)


txnBuffer = []
chain = []

state = {"Alice":[0,0]}

for i in range(0, 10):
	txnBuffer.append( [ Alice, time.time(), record, "r"])
	
for i in range(0, 20):
	txnBuffer.append( [ Alice, time.time(), record, "w"])


blockSizeLimit = 5  # Arbitrary number of transactions per block- 
               #  this is chosen by the block miner, and can vary between blocks!

while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)
    
    ## Gather a set of valid transactions for inclusion
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = isValidTxn(newTxn,state) # This will return False if txn is invalid
        
        if validTxn:           # If we got a valid state, not 'False'
            txnList.append(newTxn)
            state = updateState(newTxn,state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue  # This was an invalid transaction; ignore it and move on
        
    ## Make a block
    myBlock = makeBlock(txnList,chain)
    chain.append(myBlock)    

for item in chain:
	print(item)
	
print("Alice was naughty. She is suspended for", Alice.isSuspended, "minutes. Ha.")
