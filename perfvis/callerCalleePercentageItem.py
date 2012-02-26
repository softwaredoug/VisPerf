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
    totTime = fRecord.getRoot().getElapsedExcl()
    for rec in fRecord.getCallees():
        totTime += rec.getElapsedIncl()
    return totTime

class CallerCalleePercentageItem(AreaPercentageItem):
    def __init__(self, report, id, perc):
        AreaPercentageItem.__init__(self)
        self.report = report
        self.perc = perc
        self.funcAddr = id
        
    def __myRec(self):
        return self.report.getRecord(self.funcAddr)

    def __myEntry(self):
        return self.report.getRecord(self.funcAddr).getRoot()

    
    def getPercentage(self):
        """ Get my percentage in the parent """
        return self.perc
    
    def getName(self):
        """ Get my name, how I should be labeled on the GUI """
        return self.__myEntry().getFunctionName()
        
    def getChildren(self):
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
        totPerc = (exclPercentage + sum([item.getPercentage() for item in children]))
        assert totPerc < 100.0001
        return children
   
    def getLeftoverPerc(self):
        """ Return percentage not allocated to my children"""
        myRec = self.report.getRecord(self.funcAddr)
        totTime = totRecordTime(myRec)
        return (myRec.getRoot().getElapsedExcl() / totTime) * 100.0
    
    def getId(self):
        """ Return unique integer identifier for this item """
        return self.funcAddr

    
    def __repr__(self):
        return "CallerCalleePercentageItem(%s, %lf)" % (self.rootFunction, self.perc)
            

        
        
        
    