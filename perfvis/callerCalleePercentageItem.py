from callercallee.entry import Entry
from callercallee.funcRecord import FunctionRecord
from callercallee.report import Report
from textPerfReport import TextPerfReport

import cppName


def totRecordTime(fRecord):
    """ Sum up teh total time spent in this function
        This should be the root record's elapsed inclusive time
        but for robustness, and to tolerate weird measurement
        errors in vsperfmon, we total time spent exclusively in
        the root function + the inclusive time of the called functions
        in an ideal world, this sum should = the root's elapsed incl 
    """
    totTime = fRecord.getRoot().getElapsedExcl()
    for rec in fRecord.getCallees():
        totTime += rec.getElapsedIncl()
    return totTime


class CallerCalleePercentageItem:
    """ An item drawn in the area percent widget, represents
        a single function as navigated to from another function. 
        (note that since a function may be called my many other functions,
         this entry is not unique to this function necesarilly)"""
    def __init__(self, report, id, localPerc):
        self.report = report
        self.localPerc = localPerc
        self.funcAddr = id
        self.rtfFormattedReport = None
        self.plainTextFormattedReport = None
        
    def __createReport(self, rtf):
        report = TextPerfReport(rtf)
        
        rec = self.__myRec()
        
        callers = sorted(rec.getCallers(), key = lambda e: e.getOverallPercentage(), reverse=True)
        callees = sorted(self.createCallees(), key = lambda e: e.getLocalPercentage(), reverse=True)
            
        return report.format(functionName = self.getName(), 
                             callers = callers, 
                             callees = callees, 
                             overallPerc = self.getOverallPerc(),
                             percOfParent = self.getLocalPercentage(), 
                             localPerc = self.getLeftoverPerc())               
        
    def __myRec(self):
        return self.report.getRecord(self.funcAddr)

    def __myEntry(self):
        return self.report.getRecord(self.funcAddr).getRoot()

    
    def getLocalPercentage(self):
        """ Get my percentage of the parent I was 
            instantiated with -- aka "local" %"""
        return self.localPerc
        
    def getName(self):
        myEntry = self.__myEntry()
        shortened = cppName.smartShorten(myEntry.getFunctionName(), 100)
        return shortened
               
    def getOverallPerc(self):
        """ My percentage of the overall """
        myEntry = self.__myEntry()
        return myEntry.getOverallPercentage()
   

        
    def getFullPerfDescription(self, rtf):
        """ Format and return an RTF or plaintext description of my data"""
        if self.rtfFormattedReport == None:
            self.rtfFormattedReport = self.__createReport(rtf=True)
        if self.plainTextFormattedReport == None:
            self.plainTextFormattedReport = self.__createReport(rtf=False)
        
        if rtf:
            return self.rtfFormattedReport
        else:
            return self.plainTextFormattedReport
        
        
    def createCallees(self):
        """ Build a list of my children """
        myRec = self.__myRec()
        totTime = totRecordTime(myRec)
        exclPercentage = (myRec.getRoot().getElapsedExcl() / totTime) * 100.0
        children = []
        for callee in myRec.getCallees():
            perc = (callee.getElapsedIncl() / totTime) * 100.0
            children.append(
                            CallerCalleePercentageItem(self.report, 
                                                       callee.getFunctionAddr(),
                                                       perc)
                            )
        totPerc = (exclPercentage + sum([item.getLocalPercentage() for item in children]))
        assert totPerc < 100.0001
        return children
    
    def createCallers(self):
        """ Build a list of my parents """
        myRec = self.__myRec()
        callers = myRec.getCallers()
        return [CallerCalleePercentageItem(self.report, caller.getFunctionAddr(), caller.getOverallPercentage())
                for caller in myRec.getCallers()]
            
            
   
    def getLeftoverPerc(self):
        """ Return percentage not allocated to my children"""
        myRec = self.report.getRecord(self.funcAddr)
        totTime = totRecordTime(myRec)
        return (myRec.getRoot().getElapsedExcl() / totTime) * 100.0
    
    def getAddress(self):
        """ Return unique integer identifier for this item """
        return self.funcAddr

    
    def __repr__(self):
        return "CallerCalleePercentageItem(%s, %lf)" % (self.rootFunction, self.localPerc)
            

def sortedByPerc(items):
    """ Sort by descending percentage"""
    return sorted(items, key = lambda e: e.getLocalPercentage(), reverse=True)

        
        
    
