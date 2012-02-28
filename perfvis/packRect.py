
from PySide.QtCore import QRect, QRectF
from rectUtils import validRectReturned

class Direction:
    Horizontal = 0
    Vertical = 1
    
    @staticmethod
    def flip(direction):
        return not direction
  

class PackedRect:
    """ Given p and a starting rect, draw
        a subrectangle that takes p% of the
        area of the starting rect. Repeat for p1,p2...
        as long as there continues to be room in the parent rect"""  
    
    def __init__(self, parentRect, percentageItems, initialDir = Direction.Horizontal):
        self.parentRect = self.leftoverRect = QRectF()
        self.percItems = sorted(percentageItems, key=lambda pItem: pItem.getPercentage(), reverse = True)
        self.parentRect = QRectF(parentRect)
        self.initialDir = initialDir
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
                    perc = percItem.getPercentage()
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
        self.currDir = self.initialDir
        self.leftoverRect = copy.deepcopy(self.parentRect)
        
    def updateDirection(self, currPercentage):
        magnitude = 0
        if currPercentage > self.lastFlipPercentage and self.lastFlipPercentage > 0:
            magnitude = currPercentage / self.lastFlipPercentage
        elif currPercentage > 0:
            magnitude = self.lastFlipPercentage / currPercentage
        if magnitude > 1.5:
            self.currDir = Direction.flip(self.currDir)
            self.lastFlipPercentage = currPercentage
            
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
        remaining = QRectF(self.leftoverRect)
        self.leftoverRect.setWidth(-1)
        self.leftoverRect.setHeight(-1)
        assert self.leftoverRect.isEmpty()
        return remaining
    
    def __giveUpLeftoverHeight(self, neededArea, width, height):
        """ Sacrifice some height from the leftover rect for the needed area"""
        height = neededArea / width
        self.leftoverRect.setY(self.leftoverRect.y() + height)
        return (width, height)
        
    def __giveUpLeftoverWidth(self, neededArea, width, height):
        """ Sacrifice some width from the leftover rect for the needed area"""
        width = neededArea / height
        self.leftoverRect.setX(self.leftoverRect.x() + width)
        return (width, height)
    
    @validRectReturned    
    def __giveUpSomeLeftoverSpace(self, neededArea):
        """ Sacrifice some leftover space to represent the neededARea"""
        giveUpFns = [self.__giveUpLeftoverWidth, self.__giveUpLeftoverHeight] 
        fn = giveUpFns[self.currDir]
        newRect = QRectF()
        newRect.setTopLeft(self.leftoverRect.topLeft())
        (width, height) = (self.leftoverRect.width(), self.leftoverRect.height())
        
        (width, height) = fn(neededArea, width, height)
      
        if not self.leftoverRect.isValid():
            print "Failure with the following input"
            print "ParentRect %s" % repr(self.parentRect)
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
        
        self.updateDirection(percentage)
        
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