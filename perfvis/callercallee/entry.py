from labeledCsvEntry import LabeledCsvEntry

class Entry(object):
	
	def __findOneOfOrThrow(self, oneMustBePresent):
		for key in oneMustBePresent:
			if key in self.csvEntry.fields:
				return key
		raise ValueError("No inclusive or exclusive time could be found")
		
	
	def validateReqFieldsPresent(self):
		reqKeys = ["Function Name", "Type", "Function Address"]
		for key in reqKeys:
			if not key in self.csvEntry.fields:
				print repr(self.csvEntry.fields)
				raise ValueError("Csv input did not appear to have a field for %s" % key)
		
		self.inclusiveLabel = self.__findOneOfOrThrow(["Elapsed Inclusive Time", "Inclusive Samples"])
		self.exclusiveLabel = self.__findOneOfOrThrow(["Elapsed Exclusive Time", "Exclusive Samples"])
	
	def __init__(self, csvLine, header):
		self.csvEntry = LabeledCsvEntry(header, csvLine)
		self.validateReqFieldsPresent()	
		
	def getFunctionName(self):
		return self.csvEntry.fields["Function Name"]
	
	def getType(self):
		return self.csvEntry.fields["Type"]
	
	def getElapsedIncl(self):
		return float(self.csvEntry.fields[self.inclusiveLabel])
	
	def getElapsedExcl(self):
		return float(self.csvEntry.fields[self.exclusiveLabel])
	
	def getFunctionAddr(self):
		return int(self.csvEntry.fields["Function Address"], base=16)
	
	def __str__(self):
		return "%s,Function: %s" \
			% (self.getType(), 
				self.getFunctionName())
	
	def __repr__(self):
		return 'Entry(["%s","%s",%lf,%lf])' % \
			(self.getType(), self.getFunctionName(), 	 self.getElapsedIncl(), self.getElapsedExcl())
			
			