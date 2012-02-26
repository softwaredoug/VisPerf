from labeledCsvEntry import LabeledCsvEntry

class Entry(object):
	
	def validateReqFieldsPresent(self):
		reqKeys = ["Function Name", "Type", "Elapsed Inclusive Time", 
				   "Elapsed Exclusive Time", "Function Address"]
		for key in reqKeys:
			if not key in self.csvEntry.fields:
				print repr(self.csvEntry.fields)
				raise ValueError("Csv input did not appear to have a field for %s" % key)		
	
	def __init__(self, csvLine, header):
		self.csvEntry = LabeledCsvEntry(header, csvLine)
		self.validateReqFieldsPresent()	
		
	def getFunctionName(self):
		return self.csvEntry.fields["Function Name"]
	
	def getType(self):
		return self.csvEntry.fields["Type"]
	
	def getElapsedIncl(self):
		return float(self.csvEntry.fields["Elapsed Inclusive Time"])
	
	def getElapsedExcl(self):
		return float(self.csvEntry.fields["Elapsed Exclusive Time"])
	
	def getFunctionAddr(self):
		return int(self.csvEntry.fields["Function Address"], base=16)
	
	def __str__(self):
		return "%s,Function: %s" \
			% (self.getType(), 
				self.getFunctionName())
	
	def __repr__(self):
		return 'Entry(["%s","%s",%lf,%lf])' % \
			(self.getType(), self.getFunctionName(), 	 self.getElapsedIncl(), self.getElapsedExcl())
			
			