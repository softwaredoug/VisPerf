from entry import Entry
from entry import HdrFields

class FunctionRecord(object):
	""" A root record in the caller/callee report,
		all the callers and callees """
	def __init__(self, csvLines):
		self.entries = []
		self.parse(csvLines)
		pass
	
	def parse(self, csvLines):
		self.entries = [Entry(csvLines.pop(0))]
		while (len(csvLines) > 0):
			nextEntry = Entry(csvLines[0])
			if nextEntry.type == "Root":
				break
			self.entries.append(nextEntry)
			csvLines.pop(0)
		self.postValidate()
	
	def postValidate(self):
		if len(self.getEntriesOfType("Root")) != 1:
			self.entries = []
			raise ValueError("You attempted to construct around more than 1 Root entry")
	
	def getEntriesOfType(self, typeName):
		typeMatch = lambda ent: ent.type == typeName
		return filter(typeMatch, self.entries)
	
	def getCallers(self):
		return self.getEntriesOfType("Caller")
		
	def getCallees(self):
		return self.getEntriesOfType("Callee")
		
	def getRoot(self):
		rootRecs = self.getEntriesOfType("Root")
		assert len(rootRecs) == 1
		return rootRecs[0]
	
	def __str__(self):
		e = self.getRoot()
		return e.functionName