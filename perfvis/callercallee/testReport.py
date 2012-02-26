'''
Created on Jan 25, 2012

@author: Doug
'''
import unittest
from StringIO import StringIO
from report import Report
import csv

def strToCsvLines(aStr):
    f = StringIO(aStr)
    testRecCsv = csv.reader(f)
    #for line in testRecCsv:
    #    print line 
    lines = [line for line in testRecCsv]

    return lines


class TestReportTestCase(unittest.TestCase):
    """ Some useful asserts for convenience """


    def setUp(self):
        pass


    def tearDown(self):
        pass
    
    def usingReport(self, repStrs):
        csvLines = strToCsvLines(repStrs)
        self.report = Report(csvData = csvLines[1:], csvHeader = csvLines[0])
        
    def __findFuncRecordOfName(self, functionName):
        funcRecords = self.report.funcRecords.values()
        for funcRecord in funcRecords:
            if funcRecord.getRoot().getFunctionName() == functionName:
                funcRecord.getRoot().validateReqFieldsPresent()
                return funcRecord
        return None

    def assertReportHas(self, functionName):
        funcRecord = self.__findFuncRecordOfName(functionName)
        self.assertIsNotNone(funcRecord, "Function name %s not found" % functionName)
        pass
        
    def assertFunctionHasNCallers(self, functionName, N):
        funcRecord = self.__findFuncRecordOfName(functionName)
        self.assertIsNotNone(funcRecord, "Function name %s not found" % functionName)
        self.assertEqual(len(funcRecord.getCallers()), N, 
                         "Function name %s does not have %i callers, instead there are %i" 
                         % (functionName, N, len(funcRecord.getCallers())))
    
    def assertFunctionHasNCallees(self, functionName, N):
        funcRecord = self.__findFuncRecordOfName(functionName)
        self.assertIsNotNone(funcRecord, "Function name %s not found" % functionName)
        self.assertEqual(len(funcRecord.getCallees()), N, 
                         "Function name %s does not have %i callers, instead there are %i" 
                         % (functionName, N, len(funcRecord.getCallees())))
        
    def assertNumFuncRecordsIsN(self, N):
        self.assertEqual(len(self.report.funcRecords), N,
                         "Assertion failed, number of funcRecords not %i instead there are %i" %
                         (N, len(self.report.funcRecords)))
        
    def assertElapdeInclIsN(self, functionName, N):
        funcRecord = self.__findFuncRecordOfName(functionName)
        self.assertEqual(funcRecord.getRoot().getElapsedIncl(), N, 
                         "Elapsed inclusive for root record %s not %lf instead its %lf; entry:%s" %
                         (functionName, N, funcRecord.getRoot().getElapsedIncl(),
                         repr(funcRecord.getRoot().csvEntry.fields)))
        
    def assertElapdeExclIsN(self, functionName, N):
        funcRecord = self.__findFuncRecordOfName(functionName)
        self.assertEqual(funcRecord.getRoot().getElapsedExcl(), N, 
                         "Elapsed exclusive for root record %s not %lf instead its %lf; entry:%s" %
                         (functionName, N, funcRecord.getRoot().getElapsedExcl(), 
                          repr(funcRecord.getRoot().csvEntry.fields)))        
    
    def assertFunctionAtAddress(self, function, address):
        self.assertEqual(self.report.getRecord(address).getRoot().getFunctionName(), function,
                          "Root record %s not found at address %08x" % (function, address))

class SingleFRecordCase(TestReportTestCase):
    def testSmallRecord(self):
        self.usingReport("""Type,Function Name,Elapsed Inclusive Time,Elapsed Exclusive Time,Application Inclusive Time,Application Exclusive Time,Elapsed Inclusive Time %,Elapsed Exclusive Time %,Application Inclusive Time %,Application Exclusive Time %,Time Inclusive Probe Overhead,Time Exclusive Probe Overhead,Min Elapsed Inclusive Time,Avg Elapsed Inclusive Time,Max Elapsed Inclusive Time,Min Elapsed Exclusive Time,Avg Elapsed Exclusive Time,Max Elapsed Exclusive Time,Min Application Inclusive Time,Avg Application Inclusive Time,Max Application Inclusive Time,Min Application Exclusive Time,Avg Application Exclusive Time,Max Application Exclusive Time,Number of Calls,Source File,Function Line Number,Module Name,Module Path,Function Address,Root Function Name,Process Name,Process ID,
"Root","@_RTC_CheckStackVars@8",333,333,333,333,0.00,0.00,0.00,0.00,63,63,333,333,333,333,333,333,0,333,333,0,333,333,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F1456,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Caller","_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,"""
                    )
        
        self.assertEquals(len(self.report.funcRecords), 1, "Single function record")
        self.assertFunctionAtAddress(function = "@_RTC_CheckStackVars@8", address = 0x012F1456)
        self.assertReportHas("@_RTC_CheckStackVars@8")
        self.assertFunctionHasNCallers("@_RTC_CheckStackVars@8", N=1)
        self.assertFunctionHasNCallees("@_RTC_CheckStackVars@8", N=0)
        self.assertNumFuncRecordsIsN(N = 1)
        self.assertElapdeInclIsN("@_RTC_CheckStackVars@8", N=333)        
        self.assertElapdeExclIsN("@_RTC_CheckStackVars@8", N=333)
        
        
    def testLargerRecord(self):
        self.usingReport("""Type,Function Name,Elapsed Inclusive Time,Elapsed Exclusive Time,Application Inclusive Time,Application Exclusive Time,Elapsed Inclusive Time %,Elapsed Exclusive Time %,Application Inclusive Time %,Application Exclusive Time %,Time Inclusive Probe Overhead,Time Exclusive Probe Overhead,Min Elapsed Inclusive Time,Avg Elapsed Inclusive Time,Max Elapsed Inclusive Time,Min Elapsed Exclusive Time,Avg Elapsed Exclusive Time,Max Elapsed Exclusive Time,Min Application Inclusive Time,Avg Application Inclusive Time,Max Application Inclusive Time,Min Application Exclusive Time,Avg Application Exclusive Time,Max Application Exclusive Time,Number of Calls,Source File,Function Line Number,Module Name,Module Path,Function Address,Root Function Name,Process Name,Process ID,
"Root","___security_init_cookie",7848,5997,7848,5997,0.00,0.00,0.00,0.00,693,693,7848,7848,7848,5997,5997,5997,0,7848,7848,0,5997,5997,1,"f:\dd\vctools\crt_bld\self_x86\crt\src\gs_support.c",97,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F2A4C,"___security_init_cookie","perfPlay.exe",5068,
"Caller","_wmainCRTStartup",7848,5997,7848,5997,0.00,0.00,0.00,0.00,693,693,0,7848,7848,0,5997,5997,0,7848,7848,0,5997,5997,1,"f:\dd\vctools\crt_bld\self_x86\crt\src\crtexe.c",361,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F1760,"___security_init_cookie","perfPlay.exe",5068,
"Callee","GetCurrentProcessId",318,318,318,318,0.00,0.00,0.00,0.00,0,0,0,318,318,0,318,318,0,318,318,0,318,318,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D11F8,"___security_init_cookie","perfPlay.exe",5068,
"Callee","GetCurrentThreadId",168,168,168,168,0.00,0.00,0.00,0.00,0,0,0,168,168,0,168,168,0,168,168,0,168,168,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D1450,"___security_init_cookie","perfPlay.exe",5068,
"Callee","GetSystemTimeAsFileTime",576,576,576,576,0.00,0.00,0.00,0.00,0,0,0,576,576,0,576,576,0,576,576,0,576,576,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D34D9,"___security_init_cookie","perfPlay.exe",5068,
"Callee","GetTickCount",258,258,258,258,0.00,0.00,0.00,0.00,0,0,0,258,258,0,258,258,0,258,258,0,258,258,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D110C,"___security_init_cookie","perfPlay.exe",5068,
"Callee","QueryPerformanceCounter",531,531,531,531,0.00,0.00,0.00,0.00,0,0,0,531,531,0,531,531,0,531,531,0,531,531,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D1725,"___security_init_cookie","perfPlay.exe",5068,""")
        
        self.assertFunctionAtAddress(function = "___security_init_cookie", address = 0x012F2A4C)
        self.assertReportHas("___security_init_cookie")
        self.assertFunctionHasNCallers("___security_init_cookie", N=1)
        self.assertFunctionHasNCallees("___security_init_cookie", N=5)
        self.assertNumFuncRecordsIsN(N = 1)
        self.assertElapdeExclIsN("___security_init_cookie", N=5997)
        self.assertElapdeInclIsN("___security_init_cookie", N=7848)
        
    def testCommaInFunctionName(self):        
        self.usingReport("""Type,Function Name,Elapsed Inclusive Time,Elapsed Exclusive Time,Application Inclusive Time,Application Exclusive Time,Elapsed Inclusive Time %,Elapsed Exclusive Time %,Application Inclusive Time %,Application Exclusive Time %,Time Inclusive Probe Overhead,Time Exclusive Probe Overhead,Min Elapsed Inclusive Time,Avg Elapsed Inclusive Time,Max Elapsed Inclusive Time,Min Elapsed Exclusive Time,Avg Elapsed Exclusive Time,Max Elapsed Exclusive Time,Min Application Inclusive Time,Avg Application Inclusive Time,Max Application Inclusive Time,Min Application Exclusive Time,Avg Application Exclusive Time,Max Application Exclusive Time,Number of Calls,Source File,Function Line Number,Module Name,Module Path,Function Address,Root Function Name,Process Name,Process ID,
"Root","foo(int,double)",333,333,333,333,0.00,0.00,0.00,0.00,63,63,333,333,333,333,333,333,0,333,333,0,333,333,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F1456,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Caller","_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,"""
                    )
        self.assertFunctionAtAddress(function = "foo(int,double)", address = 0x012F1456)
        self.assertReportHas("foo(int,double)")
        self.assertElapdeInclIsN("foo(int,double)", N=333)        
        self.assertElapdeExclIsN("foo(int,double)", N=333)

        
        
class TwoFRecordCase(TestReportTestCase):
    def testTwoSmallRecord(self):
        self.usingReport("""Type,Function Name,Elapsed Inclusive Time,Elapsed Exclusive Time,Application Inclusive Time,Application Exclusive Time,Elapsed Inclusive Time %,Elapsed Exclusive Time %,Application Inclusive Time %,Application Exclusive Time %,Time Inclusive Probe Overhead,Time Exclusive Probe Overhead,Min Elapsed Inclusive Time,Avg Elapsed Inclusive Time,Max Elapsed Inclusive Time,Min Elapsed Exclusive Time,Avg Elapsed Exclusive Time,Max Elapsed Exclusive Time,Min Application Inclusive Time,Avg Application Inclusive Time,Max Application Inclusive Time,Min Application Exclusive Time,Avg Application Exclusive Time,Max Application Exclusive Time,Number of Calls,Source File,Function Line Number,Module Name,Module Path,Function Address,Root Function Name,Process Name,Process ID,
"Root","FUNCTION_1",123,444,421,444,0.00,0.00,0.00,0.00,63,63,333,333,333,333,333,333,0,333,333,0,333,333,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0xA12F1456,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Caller","_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",Bx012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Callee","not_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",Cx012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Root","FUNCTION_2",123,444,421,444,0.00,0.00,0.00,0.00,63,63,333,333,333,333,333,333,0,333,333,0,333,333,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0xD12F1456,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Caller","_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",Bx012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Callee","not_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",Cx012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,"""
                    )
        self.assertReportHas("FUNCTION_1")
        self.assertReportHas("FUNCTION_2")
        self.assertFunctionAtAddress(function = "FUNCTION_1", address = 0xA12F1456)
        self.assertFunctionAtAddress(function = "FUNCTION_2", address = 0xD12F1456)
        self.assertNumFuncRecordsIsN(N = 2)
        self.assertFunctionHasNCallees(functionName = "FUNCTION_1", N=1)       
        self.assertFunctionHasNCallers(functionName = "FUNCTION_1", N=1)
        self.assertFunctionHasNCallees(functionName = "FUNCTION_2", N=1)
        self.assertFunctionHasNCallers(functionName = "FUNCTION_2", N=1)
        self.assertElapdeExclIsN("FUNCTION_1", N=444)
        self.assertElapdeInclIsN("FUNCTION_1", N=123)
        
    def testDuplicateNames(self):
        self.usingReport("""Type,Function Name,Elapsed Inclusive Time,Elapsed Exclusive Time,Application Inclusive Time,Application Exclusive Time,Elapsed Inclusive Time %,Elapsed Exclusive Time %,Application Inclusive Time %,Application Exclusive Time %,Time Inclusive Probe Overhead,Time Exclusive Probe Overhead,Min Elapsed Inclusive Time,Avg Elapsed Inclusive Time,Max Elapsed Inclusive Time,Min Elapsed Exclusive Time,Avg Elapsed Exclusive Time,Max Elapsed Exclusive Time,Min Application Inclusive Time,Avg Application Inclusive Time,Max Application Inclusive Time,Min Application Exclusive Time,Avg Application Exclusive Time,Max Application Exclusive Time,Number of Calls,Source File,Function Line Number,Module Name,Module Path,Function Address,Root Function Name,Process Name,Process ID,
"Root","FUNCTION_1",333,555,421,444,0.00,0.00,0.00,0.00,63,63,333,333,333,333,333,333,0,333,333,0,333,333,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0xA12F1456,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Caller","_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",Bx012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Callee","not_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",Cx012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Root","FUNCTION_1",123,444,421,444,0.00,0.00,0.00,0.00,63,63,333,333,333,333,333,333,0,333,333,0,333,333,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0xD12F1456,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Caller","_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",Bx012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Callee","not_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",Cx012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,"""
                    )
        self.assertReportHas("FUNCTION_1")
        self.assertFunctionAtAddress(function = "FUNCTION_1", address = 0xA12F1456)
        self.assertFunctionAtAddress(function = "FUNCTION_1", address = 0xD12F1456)
        fRecord  = self.report.getRecord(0xA12F1456)
        self.assertEqual(fRecord.getRoot().getElapsedIncl(), 333)
        self.assertEqual(fRecord.getRoot().getElapsedExcl(), 555)        
        self.assertEqual(fRecord.getRoot().getElapsedIncl(), 333)
        self.assertEqual(fRecord.getRoot().getElapsedExcl(), 555)        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()