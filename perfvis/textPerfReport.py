'''
Created on Apr 8, 2012

@author: Doug
'''

import cppName

class TextPerfReport:
    """ Class for formatting the string used in the tool-tip for a function,
        basically a detailed breakdown of the  function's stats. Can be presented
        in either rtf or non-rtf based on the boolean rtf passed at construction
        
        Simply construct and then call "format"
        
        """
    def __init__(self, rtf):
        """ Construct, specifying whether rtf formatting is desired, if false,
            plain-text will be provided"""
        self.rtf = rtf
        self.template = self.__createTemplate()
        
    def format(self, functionName, callers, callees, overallPerc, percOfParent, localPerc):
        """ Perform formatting passing the passed in args to the template"""
        callerStr = self.__formatCallers(callers)
        calleeStr = self.__formatCallees(callees)
        valuesForTemplate = {"functionName" : self.__escapeFunc()(functionName),
                             "overallPerc" : overallPerc,
                             "calleeStr" : calleeStr,
                             "callerStr" : callerStr,
                             "percLocal" : localPerc,
                             "percOfParent" : percOfParent}
        return self.template % valuesForTemplate        
    
    def __applyFormattingToTemplate(self, templStr):
        """ Apply any formatting to the template based on whether 
            or not rtf is being used"""
        from string import Template
        templStr = templStr.rstrip("\n")
        boldBeg, boldEnd, eol, lt, gt, _ = self.__formatCfg()
        templStr = templStr.replace("\n", "${eol}")
        return Template(templStr).safe_substitute(boldBeg=boldBeg, boldEnd=boldEnd, eol=eol, lt=lt, gt=gt)

    def __formatCallers(self, callers):
        """ Format the list of callers into a string with one line
            per caller""" 
        escFunc = self.__escapeFunc()
        
        callerStr = "".join(["(%2.2lf) %s\n" % 
                                (caller.getOverallPercentage(),
                                 escFunc(cppName.smartShorten(caller.getFunctionName(), 100))) for caller in callers],
                                 )
        return self.__applyFormattingToTemplate(callerStr)
        
    
    def __formatCallees(self, callees):
        """ Format the list of callees into a string with one line
            per caller"""
        calleeStr = "".join(["${lt}%2.2lf${gt} %s\n" % 
                                  (callee.getLocalPercentage(),
                                 self.__escapeFunc()(callee.getName())) for callee in callees])       
        calleeStr = calleeStr.rstrip("\n")
        return self.__applyFormattingToTemplate(calleeStr)
        

    
    @staticmethod
    def __escapeHtml(text):
        """ taken from http://wiki.python.org/moin/EscapingHtml """
        html_escape_table = {",": ",",
                         "&": "&amp;",
                         '"': "&quot;",
                         "'": "&apos;",
                         ">": "&gt;",
                         "<": "&lt;"}
        converted = "".join(html_escape_table.get(c,c) for c in text)
        return converted
    
    def __escapeFunc(self):
        """ Get a function to apply to text from the report  for 
            escaping"""
        if self.rtf:
            return TextPerfReport.__escapeHtml
        else:
            return lambda text: text
    
    def __formatCfg(self):
        if self.rtf:
            boldBegin, boldEnd, eol,  lt, gt, escapeFunc = '<b>', '</b>', '<br>', '&lt;', '&gt;', TextPerfReport.__escapeHtml 
        else:
            boldBegin, boldEnd, eol,  lt, gt, escapeFunc = '','','\n', '<', '>', lambda text: text
        return (boldBegin, boldEnd, eol, lt, gt, escapeFunc)
        
    def __createTemplate(self):
        reportTemplate = \
"""${boldBeg}Function (Full Name)${boldEnd}:
%(functionName)s

${boldBeg}Percent of Overall Time${boldEnd}
(%(overallPerc)2.2lf)

${boldBeg}Percent of Parent${boldEnd}
${lt}%(percOfParent)2.2lf${gt}

${boldBeg}Breakdown of children${boldEnd}
%(calleeStr)s
${lt}%(percLocal)2.1lf${gt} Local Time
    
${boldBeg}Overall time (%(overallPerc)2.2lf) distributed among parents:${boldEnd}
%(callerStr)s
"""
        return self.__applyFormattingToTemplate(reportTemplate)        