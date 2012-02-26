from funcRecord import FunctionRecord
from entry import Entry


class Report:
	def __init__(self, csvData, csvHeader):
		self.funcRecords = {}
		self.parse(csvData, csvHeader)
		
	
	def parse(self, csvData, csvHeader):
		# Decode around a "Root" string, but add back in that
		# Root string
		self.funcRecords = {}
		while len(csvData) > 0:
			fRecord = FunctionRecord(csvData, csvHeader)
			funcAddr = fRecord.getRoot().getFunctionAddr()
			print "Inserting %s" % funcAddr
			self.funcRecords[funcAddr] = fRecord
		
	def getAllRecords(self):
		return self.funcRecords
	
	def getRecord(self, funcAddr):
		return self.funcRecords[funcAddr]
	
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
	import csv
	rdr = csv.reader(f)
	lines = [line for line in rdr]
	return Report(csvData = lines[1:], csvHeader = lines[0]) 
