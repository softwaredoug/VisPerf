'''
Created on Jan 25, 2012

@author: Doug
'''
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testCallerCalleeEntry(self):
        from perfvis.callercallee.entry import HdrFields
        from perfvis.callercallee.entry import Entry
        testEntry = "\"Root\",\"__RTC_Shutdown\",1080,210,1080,210,0.00,0.00,0.00,0.00,315,252,1080,1080,1080,210,210,210,0,1080,1080,0,210,210,1,"",0,\"perfPlay.exe\",\"C:\Users\Doug\Documents\Visual Studio 2010\Projects\perfPlay\Debug\perfPlay.exe\",0x012F1534,\"__RTC_Shutdown\",\"perfPlay.exe\",5068,"
        entry = Entry(testEntry)
        assert entry.getField(HdrFields.fieldType) == "Root"
        assert entry.getField(HdrFields.functionName) == "__RTC_Shutdown"
        assert entry.getField(HdrFields.elapsedIncl) == 1080
        
    def testCallerCalleeFuncRecord(self):
        pass

        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCallerCalleeEntry']
    unittest.main()