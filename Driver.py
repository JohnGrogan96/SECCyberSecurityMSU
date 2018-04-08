import User
import Group
import Activity
import DataEntry
import DataType

Bob = User()
Bob.ID = 123

personalRecords = DataType()
personalRecords.name = "Personal Records"
personalRecords.sensitivity = 7
personalRecords.frequencyOfAccess = 10
personalRecords.reviewTime = 4000
personalRecords.Immutability = 8

AlicePrivs = Privilege()
AlicePrivs.read = True
AlicePrivs.TypeOfData = "Personal Records"

AliceAct = Activity()
AliceAct.sensitivityAccesses = 10
AliceAct.accessesPerHour = 10
AliceAct.readsPerHour = 10
AliceAct.writesPerHour = 10
AliceAct.changeSecAttributes = 10

AliceAct.dataTypeAccessesPerHour.append(personalRecords, 10)
AliceAct.dataTypeReadsPerHour.append(personalRecords, 10)
AliceAct.dataTypeWritesPerHour.append(personalRecords, 10)
AliceAct.dataTypeSecAttributesPerHour.append(personalRecords, 10)

Alice = User()
Alice.email = "Someemail@domain.com"
Alice.phoneNumber = "1111111111"
Alice.name = "Alice"
Alice.privList.append(AlicePrivs)
Alice.ID = 12
Alice.managerID = 123
Alice.userActivity =  AliceAct
Alice.dataTypeAccess.append(personalRecords)


