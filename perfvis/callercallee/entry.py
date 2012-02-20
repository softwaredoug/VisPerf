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
		self.fields = csvLine.split(',')
		self.fields = [field.lstrip("\"").rstrip("\"") for field in self.fields]
		self.type = self.fields[HdrFields.fieldType]
		self.functionName = self.fields[HdrFields.functionName]
		self.elapsedIncl = float(self.fields[HdrFields.elapsedIncl])
		self.elapsedExcl = float(self.fields[HdrFields.elapsedExcl])
		
	def __str__(self):
		return "%s,Function: %s" \
			% (self.type, 
				self.functionName)