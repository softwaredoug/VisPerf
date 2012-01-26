
def createFunctionRecord(srcStr):
	from funcRecord import FunctionRecord
	return FunctionRecord(srcStr)
	

class Report:
	def __init__(self, srcStr):
		self.funcRecords = []
		self.parse(srcStr)
	
	def parse(self, srcStr):
		# Decode around a "Root" string, but add back in that
		# Root string
		funcRecordStrs = ["\"Root\"" + currStr for currStr in srcStr.split("\"Root\"")][1:]
		#from funcRecord import FunctionRecord 
		mapRes = map(createFunctionRecord, funcRecordStrs)
		self.funcRecords = mapRes
		
	def getAllRecords(self):
		return self.funcRecords
		
		