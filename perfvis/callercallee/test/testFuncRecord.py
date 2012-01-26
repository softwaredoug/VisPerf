'''
Created on Jan 25, 2012

@author: Doug
'''
import unittest
from perfvis.callercallee.entry import HdrFields

class BasicFunctionalityTest(unittest.TestCase):

    def setUp(self):
        testRecord = """"Root","__RTC_Shutdown",1080,210,1080,210,0.00,0.00,0.00,0.00,315,252,1080,1080,1080,210,210,210,0,1080,1080,0,210,210,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F1534,"__RTC_Shutdown","perfPlay.exe",5068,
"Caller","__RTC_Terminate",1080,210,1080,210,0.00,0.00,0.00,0.00,315,252,0,1080,1080,0,210,210,0,1080,1080,0,210,210,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F277A,"__RTC_Shutdown","perfPlay.exe",5068,
"Callee","THUNK:_CRT_RTC_INITW",870,234,870,234,0.00,0.00,0.00,0.00,63,63,0,870,870,0,234,234,0,870,870,0,234,234,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F2348,"__RTC_Shutdown","perfPlay.exe",5068,"""
        from perfvis.callercallee.funcRecord import FunctionRecord
        self.record = FunctionRecord(testRecord)

    def tearDown(self):
        pass

    def testGetRoot(self):
        rootRecord = self.record.getRoot()
        assert rootRecord.getField(HdrFields.fieldType) == "Root"
        assert rootRecord.getField(HdrFields.functionName) == "__RTC_Shutdown"
        
    def testGetCallee(self):
        callees = self.record.getCallees()
        assert len(callees) == 1
        assert callees[0].getField(HdrFields.fieldType) == "Callee"
        assert callees[0].getField(HdrFields.functionName) == "THUNK:_CRT_RTC_INITW"  

    def testGetCallers(self):
        callers = self.record.getCallers()
        assert len(callers) == 1    
        assert callers[0].getField(HdrFields.fieldType) == "Caller"
        assert callers[0].getField(HdrFields.functionName) == "__RTC_Terminate"
        
class TestWithTrailingNewline(unittest.TestCase):
    def setUp(self):
        testRecord = """"Root","__RTC_Shutdown",1080,210,1080,210,0.00,0.00,0.00,0.00,315,252,1080,1080,1080,210,210,210,0,1080,1080,0,210,210,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F1534,"__RTC_Shutdown","perfPlay.exe",5068,
"Caller","__RTC_Terminate",1080,210,1080,210,0.00,0.00,0.00,0.00,315,252,0,1080,1080,0,210,210,0,1080,1080,0,210,210,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F277A,"__RTC_Shutdown","perfPlay.exe",5068,
"Callee","THUNK:_CRT_RTC_INITW",870,234,870,234,0.00,0.00,0.00,0.00,63,63,0,870,870,0,234,234,0,870,870,0,234,234,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F2348,"__RTC_Shutdown","perfPlay.exe",5068,
"""
        from perfvis.callercallee.funcRecord import FunctionRecord
        self.record = FunctionRecord(testRecord)
        
    def tearDown(self):
        pass

    def testGetRoot(self):
        rootRecord = self.record.getRoot()
        assert rootRecord.getField(HdrFields.fieldType) == "Root"
        assert rootRecord.getField(HdrFields.functionName) == "__RTC_Shutdown"
        
    def testGetCallee(self):
        callees = self.record.getCallees()
        assert len(callees) == 1
        assert callees[0].getField(HdrFields.fieldType) == "Callee"
        assert callees[0].getField(HdrFields.functionName) == "THUNK:_CRT_RTC_INITW"  

    def testGetCallers(self):
        callers = self.record.getCallers()
        assert len(callers) == 1    
        assert callers[0].getField(HdrFields.fieldType) == "Caller"
        assert callers[0].getField(HdrFields.functionName) == "__RTC_Terminate"


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()