from callercallee.entry import Entry
from callercallee.funcRecord import FunctionRecord
from callercallee.report import Report

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
    
def escapeHtml(text):
    """ taken from http://wiki.python.org/moin/EscapingHtml """
    html_escape_table = {",": ",",
                         "&": "&amp;",
                         '"': "&quot;",
                         "'": "&apos;",
                         ">": "&gt;",
                         "<": "&lt;"}
    converted = "".join(html_escape_table.get(c,c) for c in text)
    return converted
    

    

class CallerCalleePercentageItem:
    """ An item drawn in the area percent widget, represents
        a single function as navigated to from another function. 
        (note that since a function may be called my many other functions,
         this entry is not unique to this function necesarilly)"""
    def __init__(self, report, id, localPerc):
        self.report = report
        self.localPerc = localPerc
        self.funcAddr = id
        
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
        
    def getFullPerfDescription(self):
        """ Format an RTF description of my data"""
        myEntry = self.__myEntry()
        rec = self.__myRec()
        addr = myEntry.getFunctionAddr()
        
       
        callers = sorted(rec.getCallers(), key = lambda e: e.getOverallPercentage(), reverse=True)
        
        calers = callers[:10]
        callerStr = "".join(["(%2.2lf) %s<br>" % 
                                (caller.getOverallPercentage(), escapeHtml(cppName.smartShorten(caller.getFunctionName(), 100))) for caller in callers],
                                 )
        
        children = self.createCallees()
        callees = sorted(children, key = lambda e: e.getLocalPercentage(), reverse=True)
        calleeStr = "".join(["&lt;%2.2lf&gt; %s<br>" % 
                                  (callee.getLocalPercentage(),
                                 escapeHtml(callee.getName())) for callee in callees])
        
        rtfStr = """<b>Function (Full Name)</b>:<br>
                    %s<br><br>
                    <b>Percent of Overall Time</b><br>
                    (%2.2lf)<br><br>
                    <b>Percent of Parent</b><br>
                    &lt;%2.2lf&gt;<br><br>
                    <b>Breakdown of children</b>:<br>
                    %s
                    &lt;%2.1lf&gt; Local Time<br><br>
                    <b>Overall time (%2.2lf) distributed among parents:</b>:<br>
                    %s<br>
                    """ % (escapeHtml(myEntry.getFunctionName()), 
                           myEntry.getOverallPercentage(), 
                           self.getLocalPercentage(),
                           calleeStr,
                           self.getLeftoverPerc(),
                           myEntry.getOverallPercentage(),
                           callerStr)
        return rtfStr
        
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

        
        
    
