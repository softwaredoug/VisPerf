from funcRecord import FunctionRecord
from entry import HdrFields
from entry import Entry

def createFunctionRecord(srcStr):
	rec = FunctionRecord(srcStr)
	fName = rec.getRoot().functionName
	return (fName, rec)
	

class Report:
	def __init__(self, srcStr):
		self.funcRecords = {}
		self.parse(srcStr)
		
	
	def parse(self, srcStr):
		# Decode around a "Root" string, but add back in that
		# Root string
		funcRecordStrs = ["\"Root\"" + currStr for currStr in srcStr.split("\"Root\"")][1:]
		#from funcRecord import FunctionRecord 
		mapRes = map(createFunctionRecord, funcRecordStrs)
		self.funcRecords = dict(mapRes)
		
	def getAllRecords(self):
		return self.funcRecords
	
	def getRecord(self, name):
		return self.funcRecords[name]
	
	def getRecordsWithLargeCallees(self):
		rVal = []
		for (_, funcRec) in self.funcRecords.items():
			root = funcRec.getRoot()
			for callee in funcRec.getCallees():
				if callee.elapsedIncl > root.elapsedIncl:
					rVal.append(funcRec)
		return rVal
					
		

def loadReport(fName):
	f = open(fName)
	return Report(f.read()) 
