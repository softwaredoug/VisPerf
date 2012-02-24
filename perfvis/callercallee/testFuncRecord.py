'''
Created on Jan 25, 2012

@author: Doug
'''
import unittest
from entry import HdrFields
import csv
from StringIO import StringIO

def strToCsvLines(aStr):
    f = StringIO(aStr)
    testRecCsv = csv.reader(f)
    #for line in testRecCsv:
    #    print line 
    lines = [line for line in testRecCsv]

    return lines


class BasicFunctionalityTest(unittest.TestCase):

    def setUp(self):
        testRecord = """"Root","__RTC_Shutdown",1080,210,1080,210,0.00,0.00,0.00,0.00,315,252,1080,1080,1080,210,210,210,0,1080,1080,0,210,210,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F1534,"__RTC_Shutdown","perfPlay.exe",5068,
"Caller","__RTC_Terminate",1080,210,1080,210,0.00,0.00,0.00,0.00,315,252,0,1080,1080,0,210,210,0,1080,1080,0,210,210,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F277A,"__RTC_Shutdown","perfPlay.exe",5068,
"Callee","THUNK:_CRT_RTC_INITW",870,234,870,234,0.00,0.00,0.00,0.00,63,63,0,870,870,0,234,234,0,870,870,0,234,234,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F2348,"__RTC_Shutdown","perfPlay.exe",5068,"""
        from funcRecord import FunctionRecord
        lines = strToCsvLines(testRecord)
        self.record = FunctionRecord(lines)

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
        from funcRecord import FunctionRecord
        lines = strToCsvLines(testRecord)
        self.record = FunctionRecord(lines)
        
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
        
class TestWithMultipleRootRecords(unittest.TestCase):
    """ Test that we only read the first ROOT record"""
    def setUp(self):
        testRecord = """"Root","__RTC_Shutdown",1080,210,1080,210,0.00,0.00,0.00,0.00,315,252,1080,1080,1080,210,210,210,0,1080,1080,0,210,210,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F1534,"__RTC_Shutdown","perfPlay.exe",5068,
"Caller","__RTC_Terminate",1080,210,1080,210,0.00,0.00,0.00,0.00,315,252,0,1080,1080,0,210,210,0,1080,1080,0,210,210,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F277A,"__RTC_Shutdown","perfPlay.exe",5068,
"Callee","THUNK:_CRT_RTC_INITW",870,234,870,234,0.00,0.00,0.00,0.00,63,63,0,870,870,0,234,234,0,870,870,0,234,234,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F2348,"__RTC_Shutdown","perfPlay.exe",5068,
"Root","___security_init_cookie",7440,6156,7440,6156,0.70,0.58,0.70,0.58,693,693,7440,7440,7440,6156,6156,6156,0,7440,7440,0,6156,6156,1,"f:\dd\vctools\crt_bld\self_x86\crt\src\gs_support.c",97,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x01142A14,"___security_init_cookie","perfPlay.exe",3320,
"Caller","_wmainCRTStartup",7440,6156,7440,6156,0.70,0.58,0.70,0.58,693,693,0,7440,7440,0,6156,6156,0,7440,7440,0,6156,6156,1,"f:\dd\vctools\crt_bld\self_x86\crt\src\crtexe.c",361,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x01141758,"___security_init_cookie","perfPlay.exe",3320,
"Callee","GetCurrentProcessId",258,258,258,258,0.02,0.02,0.02,0.02,0,0,0,258,258,0,258,258,0,258,258,0,258,258,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x751B11F8,"___security_init_cookie","perfPlay.exe",3320,
"Callee","GetCurrentThreadId",153,153,153,153,0.01,0.01,0.01,0.01,0,0,0,153,153,0,153,153,0,153,153,0,153,153,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x751B1450,"___security_init_cookie","perfPlay.exe",3320,
"Callee","GetSystemTimeAsFileTime",369,369,369,369,0.03,0.03,0.03,0.03,0,0,0,369,369,0,369,369,0,369,369,0,369,369,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x751B34D9,"___security_init_cookie","perfPlay.exe",3320,
"Callee","GetTickCount",183,183,183,183,0.02,0.02,0.02,0.02,0,0,0,183,183,0,183,183,0,183,183,0,183,183,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x751B110C,"___security_init_cookie","perfPlay.exe",3320,
"Callee","QueryPerformanceCounter",321,321,321,321,0.03,0.03,0.03,0.03,0,0,0,321,321,0,321,321,0,321,321,0,321,321,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x751B1725,"___security_init_cookie","perfPlay.exe",3320,
"""
        from funcRecord import FunctionRecord
        lines = strToCsvLines(testRecord)
        self.record = FunctionRecord(lines)
        self.record2 = FunctionRecord(lines)
        
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
        
    def testParseTwoEntrys(self):
        rootEntry = self.record2.getRoot()
        assert rootEntry.getField(HdrFields.fieldType) == "Root"
        assert rootEntry.getField(HdrFields.functionName) == "___security_init_cookie"
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()