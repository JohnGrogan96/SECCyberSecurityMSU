class Activity:
	def __init__(self):
		self.sensitivityAccesses = None
		self.accessesPerHour = None
		self.readsPerHour = None
		self.writesPerHour = None
		self.changeSecAttributes = None

		self.dataTypeAccessesPerHour = []
		self.dataTypeReadsPerHour = []
		self.dataTypeWritesPerHour = []
		self.dataTypeSecAttributesPerHour = []
