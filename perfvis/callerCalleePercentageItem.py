from areaPercentageWidget import AreaPercentageItem
from callercallee.entry import Entry
from callercallee.funcRecord import FunctionRecord
from callercallee.report import Report


def totRecordTime(fRecord):
    """ Sum up teh total time spent in this function
        This should be the root record's elapsed inclusive time
        but for robustness, and to tolerate weird measurement
        errors in vsperfmon, we total time spent exclusively in
        the root function + the inclusive time of the called functions
        in an ideal world, this sum should = the root's elapsed incl 
    """
    totTime = fRecord.getRoot().elapsedExcl
    for rec in fRecord.getCallees():
        totTime += rec.elapsedIncl
    return totTime

class CallerCalleePercentageItem(AreaPercentageItem):
    def __init__(self, report, rootFunction, perc):
        AreaPercentageItem.__init__(self)
        self.report = report
        self.rootFunction = rootFunction
        self.perc = perc
        
    def __myRec(self):
        return self.report.getRecord(self.rootFunction)

    def __myEntry(self):
        return self.report.getRecord(self.rootFunction).getRoot()

    
    def getPercentage(self):
        """ Get my percentage in the parent """
        return self.perc
    
    def getName(self):
        """ Get my name, how I should be labeled on the GUI """
        return self.rootFunction # + "\n%.0lf" % self.__myEntry().elapsedIncl
        
    def getChildren(self):
        """ Build a list of my children """
        myRec = self.__myRec()
        totTime = totRecordTime(myRec)
        exclPercentage = (myRec.getRoot().elapsedExcl / totTime) * 100.0
        children = []
        for callee in myRec.getCallees():
            perc = (callee.elapsedIncl / totTime) * 100.0
            children.append(
                            CallerCalleePercentageItem(self.report, 
                                                       callee.functionName,
                                                       perc))
        totPerc = (exclPercentage + sum([item.getPercentage() for item in children]))
        assert totPerc < 100.0001
        return children
    
    def __repr__(self):
        return "CallerCalleePercentageItem(%s, %lf)" % (self.rootFunction, self.perc)
            
        
        
        #sum the callees and the 
    
    def getLeftoverPerc(self):
        myRec = self.report.getRecord(self.rootFunction)
        totTime = totRecordTime(myRec)
        return (myRec.getRoot().elapsedExcl / totTime) * 100.0

        
        
        
    