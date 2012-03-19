import packRect
import unittest
from PySide.QtCore import QRectF

class TestPercItem:
    def __init__(self, localPerc):
        self.localPerc = localPerc
        
    def getLocalPercentage(self):
        print "returning %lf" % self.localPerc
        return self.localPerc
    
    def __str__(self):
        return "Perc %lf" % self.localPerc
    
    def __repr__(self):
        return "TestPercItem(%lf)" % self.localPerc
    
def TestPercItemsFromPercList(percList):
    rVal = [TestPercItem(perc) for perc in percList]
    print rVal
    return rVal

class TestPackedRect(unittest.TestCase):
    def __assertIsContainedWithin(self, parentRect, childRect):
        intersected = parentRect.intersected(childRect)
        print "Intersected %s" % intersected
        self.assertAlmostEqual(intersected.height(), childRect.height(), delta = 0.00001)
        self.assertAlmostEqual(intersected.width(), childRect.width(), delta = 0.00001)
        self.assertAlmostEqual(intersected.x(), childRect.x(), delta = 0.00001)
        self.assertAlmostEqual(intersected.y(), childRect.y(), delta = 0.00001)
    
    def __assertIsApproxPercOfArea(self, parentRect, childRect, percentage):
        chArea = childRect.width() * childRect.height()
        parentArea = parentRect.width() * parentRect.height()
        print "Percentage: %lf " % (percentage)
        self.assertAlmostEqual(chArea, parentArea * (percentage/100.0), 2)
    
    def __assertDoesNotOverlapSiblings(self, parentRect, childRect, siblRects):
        for rect in siblRects:
            self.assertFalse(rect.intersects(childRect), 
                             "childRect %s intersects with sibl %s parent is %s" %
                             (childRect, rect, parentRect))
                
        pass
    
    def __confirmGivesValidOutput(self, parentRect, percentages):
        percItems = TestPercItemsFromPercList(percentages)
        pR = packRect.PackedRect(parentRect, percItems)
        sibls = []
        print "sum: %i" % sum(percentages) 
        try:
            for (chItem, nextChRect) in pR:
               
                self.__assertIsContainedWithin(parentRect, nextChRect)
                self.__assertIsApproxPercOfArea(parentRect, nextChRect, chItem.getLocalPercentage())
                self.__assertDoesNotOverlapSiblings(parentRect, nextChRect, sibls)
                sibls.append(nextChRect)

        except ValueError as e:
            raise self.fail(e)
        
    def testValidInputs(self):
        self.__confirmGivesValidOutput(parentRect = QRectF(0,0,640,480),
                                       percentages = [50,20,10])
        self.__confirmGivesValidOutput(parentRect = QRectF(0,0,354,419),
                                       percentages = [0.0112117175903,
                                                      0.212574165512,
                                                      0.00078482023132,
                                                      80.6474916398,
                                                      0.03228974666,
                                                      0.00695126490598,
                                                      0.00515739009153,
                                                      17.1050448244,
                                                      1.95293171466])
        self.__confirmGivesValidOutput(parentRect = QRectF(2,3,10,595),
                                       percentages = [99.1963661775])
        
        self.__confirmGivesValidOutput(parentRect = QRectF(2.000000, 30.000000, 42.000000, 733.000000),
                                        percentages = [68.3650150618, 29.5471070946])
        
        self.__confirmGivesValidOutput(parentRect = QRectF(2.000000, 30.000000, 16.000000, 664.000000),
                                        percentages = [99.7644913773])
        self.__confirmGivesValidOutput(parentRect = QRectF(2.000000, 30.000000, 42.000000, 733.000000), 
                                       percentages = [68.36501506180534, 29.547107094629688, 2.0878778435649736])
        self.__confirmGivesValidOutput(parentRect = QRectF(2.000000, 30.000000, 564.000000, 733.000000), 
                                       percentages = [86.78029430348707, 13.217538681222926, 0.0021670152900036726, 0.0])
        

if __name__ == '__main__':
    unittest.main()