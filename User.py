class User:
	def __init__(self):
		self.email = ""
		self.phoneNumber = ""
		self.name = ""
		self.privList = []
		self.manager = None
		self.userActivity = None
		self.groups = []
		self.dataTypeAccess = []
		self.SuspendedDataTypes = []
		self.isSuspended = 0

