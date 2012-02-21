import packRect
import unittest
from PySide.QtCore import QRectF

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
        pR = packRect.PackedRect(parentRect)
        currPerc = 0
        sibls = []
        print "sum: %i" % sum(percentages) 
        try:
            for currPerc in percentages:
                nextChRect = pR.nextRect(currPerc)
                self.__assertIsContainedWithin(parentRect, nextChRect)
                self.__assertIsApproxPercOfArea(parentRect, nextChRect, currPerc)
                self.__assertDoesNotOverlapSiblings(parentRect, nextChRect, sibls)
                sibls.append(nextChRect)
                if pR.isEmpty():
                    break
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

if __name__ == '__main__':
    unittest.main()