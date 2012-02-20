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
    
    def getPercentage(self):
        """ Get my percentage in the parent """
        return self.perc
    
    def getName(self):
        """ Get my name, how I should be labeled on the GUI """
        return self.rootFunction
        
    def getChildren(self):
        """ Build a list of my children """
        myRec = self.report.getRecord(self.rootFunction)
        totTime = totRecordTime(myRec)
        exclPercentage = (myRec.getRoot().elapsedExcl / totTime) * 100.0
        children = []
        print "Children of %s" % (self.rootFunction)
        for callee in myRec.getCallees():
            perc = (callee.elapsedIncl / totTime) * 100.0
            children.append(
                            CallerCalleePercentageItem(self.report, 
                                                       callee.functionName,
                                                       perc))
        assert (exclPercentage + sum([item.getPercentage() for item in children])) <= 100.0
        return children
            
        
        
        #sum the callees and the 
    
    def getLeftoverPerc(self):
        myRec = self.report.getRecord(self.rootFunction)
        totTime = totRecordTime(myRec)
        return (myRec.getRoot().elapsedExcl / totTime) * 100.0

        
        
        
    