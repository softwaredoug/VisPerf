from funcRecord import FunctionRecord
from entry import HdrFields
from entry import Entry


class Report:
	def __init__(self, srcStr):
		self.funcRecords = {}
		self.parse(srcStr)
		
	
	def parse(self, srcCsvLines):
		# Decode around a "Root" string, but add back in that
		# Root string
		self.funcRecords = {}
		while len(srcCsvLines) > 0:
			fRecord = FunctionRecord(srcCsvLines)
			rootName = fRecord.getRoot().functionName
			print "Inserting %s" % rootName
			self.funcRecords[rootName] = fRecord
		
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
	import csv
	rdr = csv.reader(f)
	lines = [line for line in rdr]
	return Report(lines[1:]) 
