class HdrFields:
	""" Type as taken from the header in the caller/callee report"""
	fieldType = 0
	functionName = 1
	elapsedIncl = 2
	elapsedExcl = 3
	applicationIncl = 4
	applicationExcl = 5
	
	minField = fieldType
	maxField = applicationExcl

class Entry(object):
	
	def __init__(self, csvLine):
		self.fields = csvLine
		self.type = self.fields[HdrFields.fieldType]
		self.functionName = self.fields[HdrFields.functionName]
		self.elapsedIncl = float(self.fields[HdrFields.elapsedIncl])
		self.elapsedExcl = float(self.fields[HdrFields.elapsedExcl])
		
	def getField(self, idx):
		return self.fields[idx]
		
	def __str__(self):
		return "%s,Function: %s" \
			% (self.type, 
				self.functionName)
	
	def __repr__(self):
		return 'Entry(["%s","%s",%lf,%lf])' % \
			(self.type, self.functionName, self.elapsedIncl, self.elapsedExcl)