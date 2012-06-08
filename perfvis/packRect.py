
from PySide.QtCore import QRect
from rectUtils import validRectReturned
from math import ceil

class Direction:
    Horizontal = 0
    Vertical = 1
    
    @staticmethod
    def flip(direction):
        return not direction
    
class TestItem:
    def __init__(self, perc):
        self.perc = perc
        
    def getLocalPercentage(self):
        return self.perc
  

class PackedRect:
    """ Given p and a starting rect, draw
        a subrectangle that takes <= p% of the
        area of the starting rect. Repeat for p1,p2...
        as long as there continues to be room in the parent rect"""  
    
    def __init__(self, parentRect, percentageItems):
        self.parentRect = self.leftoverRect = QRect()
        self.percItems = sorted(percentageItems, key=lambda pItem: pItem.getLocalPercentage(), reverse = True)
        self.parentRect = QRect(parentRect)
        self.reset()
        self.percs = []
        
    def __iter__(self):
        return self
        
    def next(self):
        perc = 0
        if self.currPercItem < len(self.percItems) and not self.isEmpty():
            while perc == 0:
                if self.currPercItem < len(self.percItems):
                    percItem = self.percItems[self.currPercItem]
                    perc = percItem.getLocalPercentage()
                else:
                    raise StopIteration()
                self.currPercItem += 1
            
            return (percItem, self.nextRect(perc))
        else:
            raise StopIteration()
        
        
    def reset(self):
        import copy
        self.lastFlipPercentage = 100
        self.currPercItem = 0
        self.leftoverRect = QRect(self.parentRect)
        
    def __updateDirectionToPreferSquareness(self, neededArea):
        """ Pick a direction that will give a more square 
            result for the next rectangle, but strongly
            bias toward horizontal. Its important for there
            to be consistency in this algorithm and not 
            have it depend on any weird side effects """
        biasTowardHoriz = 1.5
        (width, height) = (self.leftoverRect.width(),self.leftoverRect.height())
        (width, height) = self.__calculaceGivingUpWidth(neededArea, width, height)
        widthDiff = abs(width-height) 
        (width, height) = (self.leftoverRect.width(),self.leftoverRect.height())
        (width, height) = self.__calculateGivingUpHeight(neededArea, width, height)
        heightDiff = abs(width-height)
        if widthDiff < (heightDiff * biasTowardHoriz):
            return Direction.Horizontal
        else:
            return Direction.Vertical
        
            
    def isEmpty(self):
        return self.leftoverRect.isEmpty()
    
    def __isNeededAreaMoreThanLeftover(self, neededArea):
        leftoverArea = self.leftoverRect.width() * self.leftoverRect.height()
        return (neededArea + 0.01) > leftoverArea

        
            
    @validRectReturned
    def __giveUpAllRemainingArea(self):
        """ Return all remaining leftover space and empty
            the leftover rect"""
        assert not self.leftoverRect.isEmpty()
        remaining = QRect(self.leftoverRect)
        self.leftoverRect.setWidth(-1)
        self.leftoverRect.setHeight(-1)
        assert self.leftoverRect.isEmpty()
        return remaining
    
    def __calculateGivingUpHeight(self, neededArea, width, height):
        height = neededArea / width
        height = ceil(height)
        return (width, height)
        
    def __calculaceGivingUpWidth(self, neededArea, width, height):
        width = neededArea / height
        width = ceil(width)
        return (width, height)
        
    
    def __giveUpLeftoverHeight(self, neededArea, width, height):
        """ Sacrifice some height from the leftover rect for the needed area"""
        (width, height) = self.__calculateGivingUpHeight(neededArea, width, height)
        self.leftoverRect.setY(self.leftoverRect.y() + height)
        return (width, height)
        
    def __giveUpLeftoverWidth(self, neededArea, width, height):
        """ Sacrifice some width from the leftover rect for the needed area"""
        (width, height) = self.__calculaceGivingUpWidth(neededArea, width, height)
        self.leftoverRect.setX(self.leftoverRect.x() + width)
        return (width, height)
    
    @validRectReturned    
    def __giveUpSomeLeftoverSpace(self, neededArea):
        """ Sacrifice some leftover space to represent the neededARea"""
        thisDir = self.__updateDirectionToPreferSquareness(neededArea)
        giveUpFns = [self.__giveUpLeftoverWidth, self.__giveUpLeftoverHeight] 
        fn = giveUpFns[thisDir]
        newRect = QRect()
        newRect.setTopLeft(self.leftoverRect.topLeft())
        (width, height) = (self.leftoverRect.width(), self.leftoverRect.height())
        
        (width, height) = fn(neededArea, width, height)
      
        if not self.leftoverRect.isValid() and not self.leftoverRect.isEmpty():
            print "Failure with the following input"
            print "W/H %i/%i" % (width, height)
            print "ParentRect %s" % repr(self.parentRect)
            print "Leftover %s" % repr(self.leftoverRect)
            print "Percentages %s" % repr(self.percs)

            assert False
        
        newRect.setHeight(height)
        newRect.setWidth(width)
        return newRect

        
    @validRectReturned
    def nextRect(self, percentage):
        """ Get the next rect from leftoverRect, update
            leftoverRect with whats leftover """
        self.percs.append(percentage)
        if self.isEmpty():
            raise ValueError("This guy is empty pR: %s perc: %s" % (self.parentRect, self.percs))
        neededArea = (self.parentRect.width() * self.parentRect.height()) * (percentage/100.0)
        if self.__isNeededAreaMoreThanLeftover(neededArea):
            return self.__giveUpAllRemainingArea()
        
        return self.__giveUpSomeLeftoverSpace(neededArea)
    
    def __repr__(self):
        return "PackedRect(%s)" % repr(self.parentRect) 

    def __str__(self):
        return self.__repr__() + " Leftover(%s)" % repr(self.leftoverRect)
    
emptyPackedRect = PackedRect(QRect(), [])
    
def childRects(packedRect, percentages):
    """ Given percentages and a parent packed rect,
        generate the child rects """
    for perc in percentages:
        yield packedRect.nextRect(perc)