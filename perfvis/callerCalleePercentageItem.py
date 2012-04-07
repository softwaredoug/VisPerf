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

def escapeFunc(rtf):
    if rtf:
        return escapeHtml
    else:
        return noop
    
def formatCfg(rtf):
    if rtf:
        boldBegin, boldEnd, eol,  lt, gt, escapeFunc = '<b>', '</b>', '<br>', '&lt;', '&gt;', escapeHtml 
    else:
        boldBegin, boldEnd, eol,  lt, gt, escapeFunc = '','','\n', '<', '>', noop
    return (boldBegin, boldEnd, eol, lt, gt, escapeFunc)
    


    

def noop(text):
    return text


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
    
    def __formatCallers(self, rtf):
        rec = self.__myRec()
        callers = sorted(rec.getCallers(), key = lambda e: e.getOverallPercentage(), reverse=True)
        
        escFunc = escapeFunc(rtf)
        
        calers = callers[:10]
        callerStr = "".join(["(%2.2lf) %s${eol}" % 
                                (caller.getOverallPercentage(),
                                 escFunc(cppName.smartShorten(caller.getFunctionName(), 100))) for caller in callers],
                                 )
        return callerStr

    def __formatCallees(self, rtf):
        children = self.createCallees()
        callees = sorted(children, key = lambda e: e.getLocalPercentage(), reverse=True)
        calleeStr = "".join(["${lt}%2.2lf${gt} %s${eol}" % 
                                  (callee.getLocalPercentage(),
                                 escapeFunc(rtf)(callee.getName())) for callee in callees])
        return calleeStr
    

        
    def getFullPerfDescription(self, rtf):
        from string import Template
        """ Format an RTF description of my data"""
        myEntry = self.__myEntry()
        rec = self.__myRec()
        addr = myEntry.getFunctionAddr()
        
       
        callerStr = self.__formatCallers(rtf)
        calleeStr = self.__formatCallees(rtf)
        
        boldBeg, boldEnd, eol, lt, gt, escapeFunc = formatCfg(rtf)
        
        rtfTemplate = """${boldBeg}Function (Full Name)${boldEnd}:${eol}%s${eol}${eol}${boldBeg}Percent of Overall Time${boldEnd}${eol}(%2.2lf)${eol}${eol}${boldBeg}Percent of Parent${boldEnd}${eol}${lt}%2.2lf${gt}${eol}${eol}${boldBeg}Breakdown of children${boldEnd}:${eol}%s${lt}%2.1lf${gt} Local Time${eol}${eol}${boldBeg}Overall time (%2.2lf) distributed among parents:${boldEnd}:${eol}%s${eol}""" % (escapeFunc(myEntry.getFunctionName()), 
                           myEntry.getOverallPercentage(), 
                           self.getLocalPercentage(),
                           calleeStr,
                           self.getLeftoverPerc(),
                           myEntry.getOverallPercentage(),
                           callerStr)
        
        return Template(rtfTemplate).substitute(boldBeg=boldBeg, boldEnd=boldEnd, eol=eol, lt=lt, gt=gt)
        
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

        
        
    
