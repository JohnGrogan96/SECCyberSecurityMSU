#Priviledge class file

class Priviledge:
	
	def __init__(self):
		self.read = False
		self.write = False
	
	def checkForExistence(self):
		throw NotImplementedError
		
	def changeDataPriviledge(self):
		throw NotImplementedError