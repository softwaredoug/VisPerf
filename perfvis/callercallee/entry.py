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

class Entry:
	
	def __init__(self, csvLine):
		self.fields = csvLine.split(',')
		self.fields = [field.lstrip("\"").rstrip("\"") for field in self.fields]
		for i in range(HdrFields.elapsedIncl, HdrFields.applicationExcl+1):
			self.fields[i] = int(self.fields[i]) 
		
	def getField(self, fieldId):
		if (fieldId < HdrFields.minField) or (fieldId > HdrFields.maxField):
			raise IndexError()
		else:
			return self.fields[fieldId]