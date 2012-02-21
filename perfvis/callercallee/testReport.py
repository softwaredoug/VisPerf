'''
Created on Jan 25, 2012

@author: Doug
'''
import unittest


class BasicFunctionalityTests(unittest.TestCase):


    def setUp(self):
        from perfvis.callercallee.report import Report
        basicReport = """"Root","@_RTC_CheckStackVars@8",333,333,333,333,0.00,0.00,0.00,0.00,63,63,333,333,333,333,333,333,0,333,333,0,333,333,1,"",0,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F1456,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Caller","_wmain",333,333,333,333,0.00,0.00,0.00,0.00,63,63,0,333,333,0,333,333,0,333,333,0,333,333,1,"c:\users\doug\documents\visual studio 2010\projects\perfplay\perfplay\perfplay.cpp",87,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F11C2,"@_RTC_CheckStackVars@8","perfPlay.exe",5068,
"Root","___CxxSetUnhandledExceptionFilter",37155,27,37155,27,0.00,0.00,0.00,0.00,189,189,37155,37155,37155,27,27,27,0,37155,37155,0,27,27,1,"f:\dd\vctools\crt_bld\self_x86\crt\prebuild\eh\unhandld.cpp",86,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F25C3,"___CxxSetUnhandledExceptionFilter","perfPlay.exe",5068,
"Caller","__initterm_e",37155,27,37155,27,0.00,0.00,0.00,0.00,189,189,0,37155,37155,0,27,27,0,37155,37155,0,27,27,1,"f:\dd\vctools\crt_bld\self_x86\crt\src\crt0dat.c",908,"MSVCR100D.dll","C:\Windows\system32\MSVCR100D.dll",0x60248680,"___CxxSetUnhandledExceptionFilter","perfPlay.exe",5068,
"Callee","SetUnhandledExceptionFilter",37128,37128,37128,37128,0.00,0.00,0.00,0.00,0,0,0,37128,37128,0,37128,37128,0,37128,37128,0,37128,37128,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D8799,"___CxxSetUnhandledExceptionFilter","perfPlay.exe",5068,
"Root","___security_init_cookie",7848,5997,7848,5997,0.00,0.00,0.00,0.00,693,693,7848,7848,7848,5997,5997,5997,0,7848,7848,0,5997,5997,1,"f:\dd\vctools\crt_bld\self_x86\crt\src\gs_support.c",97,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F2A4C,"___security_init_cookie","perfPlay.exe",5068,
"Caller","_wmainCRTStartup",7848,5997,7848,5997,0.00,0.00,0.00,0.00,693,693,0,7848,7848,0,5997,5997,0,7848,7848,0,5997,5997,1,"f:\dd\vctools\crt_bld\self_x86\crt\src\crtexe.c",361,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F1760,"___security_init_cookie","perfPlay.exe",5068,
"Callee","GetCurrentProcessId",318,318,318,318,0.00,0.00,0.00,0.00,0,0,0,318,318,0,318,318,0,318,318,0,318,318,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D11F8,"___security_init_cookie","perfPlay.exe",5068,
"Callee","GetCurrentThreadId",168,168,168,168,0.00,0.00,0.00,0.00,0,0,0,168,168,0,168,168,0,168,168,0,168,168,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D1450,"___security_init_cookie","perfPlay.exe",5068,
"Callee","GetSystemTimeAsFileTime",576,576,576,576,0.00,0.00,0.00,0.00,0,0,0,576,576,0,576,576,0,576,576,0,576,576,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D34D9,"___security_init_cookie","perfPlay.exe",5068,
"Callee","GetTickCount",258,258,258,258,0.00,0.00,0.00,0.00,0,0,0,258,258,0,258,258,0,258,258,0,258,258,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D110C,"___security_init_cookie","perfPlay.exe",5068,
"Callee","QueryPerformanceCounter",531,531,531,531,0.00,0.00,0.00,0.00,0,0,0,531,531,0,531,531,0,531,531,0,531,531,1,"",0,"kernel32.dll","C:\Windows\syswow64\kernel32.dll",0x761D1725,"___security_init_cookie","perfPlay.exe",5068,
"Root","___set_app_type",669,669,669,669,0.00,0.00,0.00,0.00,0,0,669,669,669,669,669,669,0,669,669,0,669,669,1,"f:\dd\vctools\crt_bld\self_x86\crt\src\errmode.c",87,"MSVCR100D.dll","C:\Windows\system32\MSVCR100D.dll",0x60245130,"___set_app_type","perfPlay.exe",5068,
"Caller","pre_c_init",669,669,669,669,0.00,0.00,0.00,0.00,0,0,0,669,669,0,669,669,0,669,669,0,669,669,1,"f:\dd\vctools\crt_bld\self_x86\crt\src\crtexe.c",197,"perfPlay.exe","C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe",0x012F15AC,"___set_app_type","perfPlay.exe",5068,"""
        self.report = Report(basicReport) 


    def tearDown(self):
        pass


    def testGetAll(self):
        funcRecords = self.report.getAllRecords()
        from perfvis.callercallee.entry import HdrFields
        assert funcRecords[0].getRoot().getField(HdrFields.functionName) == "@_RTC_CheckStackVars@8"


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()