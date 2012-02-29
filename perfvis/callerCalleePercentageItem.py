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
    
def escapeHtml(text):
    """ taken from http://wiki.python.org/moin/EscapingHtml """
    return text
    html_escape_table = {",": ", ","&": "&amp;",'"': "&quot;","'": "&apos;",">": "&gt;","<": "&lt;",}
    return "".join(html_escape_table.get(c,c) for c in text)
    
def shortenCppFunc(str):
    withoutParams = str.split("(")
    return withoutParams[0]
    

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
        
    def getBasicName(self):
        myEntry = self.__myEntry()
        shortened = shortenCppFunc(myEntry.getFunctionName())
        return shortened[-100:]
        
    def getName(self):
        """ Get my name, how I should be labeled on the GUI """
        myEntry = self.__myEntry()
        baseName = self.getBasicName()
        overallPerc = myEntry.getOverallPercentage()
        rVal =  baseName + " - " + str(self.getPercentage())[:4] + "(" + str(overallPerc)[:4] + ")"
        return rVal[-100:]
        
    def getOverallPerc(self):
        myEntry = self.__myEntry()
        return myEntry.getOverallPercentage()
        
    def getRtfDescription(self):
        myEntry = self.__myEntry()
        rec = self.__myRec()
        addr = myEntry.getFunctionAddr()
        
        callers = sorted(rec.getCallers(), key = lambda e: e.getOverallPercentage(), reverse=True)
        calers = callers[:10]
        callerStr = "".join(["(%2.1lf) %s<br>" % 
                                (caller.getOverallPercentage(),
                                 escapeHtml(shortenCppFunc(caller.getFunctionName())[-100:])) for caller in callers])
        
        children = self.getChildren()
        callees = sorted(children, key = lambda e: e.getPercentage(), reverse=True)
        calleeStr = "".join(["%2.1lf (%2.1lf) %s<br>" % 
                                (callee.getPercentage(),
                                 callee.getOverallPerc(),
                                 escapeHtml(callee.getBasicName())) for callee in callees])
        
        rtfStr = """<b>Function (Full Name)</b>:<br>
                    %s<br>
                    <b>Callers</b>:<br>
                    %s<br>
                    <b>Callees</b>:<br>
                    %s<br>
                    <b>Local Percentage</b><br>
                    %2.1lf<br>
                    """ % (escapeHtml(myEntry.getFunctionName()), callerStr, calleeStr, self.getLeftoverPerc())
        return rtfStr
        
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
            

        
        
        
    