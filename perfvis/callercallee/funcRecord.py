

class FunctionRecord:
	""" A root record in the caller/callee report,
		all the callers and callees """
	def __init__(self, srcStr):
		self.entries = []
		self.parse(srcStr)
		pass
	
	def parse(self, srcStr):
		from entry import Entry
		srcStr = srcStr.rstrip().lstrip()
		self.entries = [Entry(line) for line in srcStr.split("\n")]
		self.postValidate()
		pass
	
	def postValidate(self):
		if len(self.getEntriesOfType("Root")) != 1:
			self.entries = []
			raise ValueError("You attempted to construct around more than 1 Root entry")
	
	def getEntriesOfType(self, typeName):
		from entry import HdrFields;
		typeMatch = lambda ent: ent.getField(HdrFields.fieldType) == typeName
		return filter(typeMatch, self.entries)
	
	def getCallers(self):
		return self.getEntriesOfType("Caller")
		
	def getCallees(self):
		return self.getEntriesOfType("Callee")
		
	def getRoot(self):
		rootRecs = self.getEntriesOfType("Root")
		assert len(rootRecs) == 1
		return rootRecs[0]