
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
    
    def __init__(self, parentRect, percentageItems):
        self.parentRect = self.leftoverRect = QRectF()
        self.percItems = sorted(percentageItems, key=lambda pItem: pItem.getPercentage(), reverse = True)
        self.parentRect = QRectF(parentRect)
        print "PackedRect Created with %s and %s" % (str(parentRect), repr(self.percItems))
        self.reset()
        self.percs = []
        
    def __iter__(self):
        return self
        
    def next(self):
        print "next called"
        perc = 0
        if self.currPercItem < len(self.percItems) and not self.isEmpty():
            while perc == 0:
                print "self.percItem: %i" % self.currPercItem
                if self.currPercItem < len(self.percItems):
                    percItem = self.percItems[self.currPercItem]
                    perc = percItem.getPercentage()
                else:
                    print "stopping"
                    raise StopIteration()
                self.currPercItem += 1
            print "From next, using perc %s" % percItem
            
            return (percItem, self.nextRect(perc))
        else:
            print "Stopping iteration"
            raise StopIteration()
        
        
    def reset(self):
        import copy
        self.lastFlipPercentage = 100
        self.currPercItem = 0
        self.currDir = Direction.Horizontal
        self.leftoverRect = copy.deepcopy(self.parentRect)
        
    def updateDirection(self, currPercentage):
        magnitude = 0
        if currPercentage > self.lastFlipPercentage and self.lastFlipPercentage > 0:
            magnitude = currPercentage / self.lastFlipPercentage
        elif currPercentage > 0:
            magnitude = self.lastFlipPercentage / currPercentage
        if magnitude > 3.0:
            print "Flip..."
            self.currDir = Direction.flip(self.currDir)
            self.lastFlipPercentage = currPercentage
            
    def isEmpty(self):
        return self.leftoverRect.isEmpty()
    
    def __isNeededAreaMoreThanLeftover(self, neededArea):
        leftoverArea = self.leftoverRect.width() * self.leftoverRect.height()
        print "NA: %lf, LA %lf" % (neededArea, leftoverArea)
        return (neededArea + 0.01) > leftoverArea

        
            
    @validRectReturned
    def __giveUpAllRemainingArea(self):
        """ Return all remaining leftover space and empty
            the leftover rect"""
        assert not self.leftoverRect.isEmpty()
        print "Giving up remaining..."
        remaining = QRectF(self.leftoverRect)
        self.leftoverRect.setWidth(-1)
        self.leftoverRect.setHeight(-1)
        assert self.leftoverRect.isEmpty()
        return remaining
    
    def __giveUpLeftoverHeight(self, neededArea, width, height):
        """ Sacrifice height from the leftover rect for the needed area"""
        height = neededArea / width
        print "Vertical..., na %lf width %lf height %lf" % (neededArea, width, height)
        self.leftoverRect.setY(self.leftoverRect.y() + height)
        return (width, height)
        
    def __giveUpLeftoverWidth(self, neededArea, width, height):
        """ Sacrifice width from the leftover rect for the needed area"""
        width = neededArea / height
        print "Horizontal..., na %lf width %lf height %lf" % (neededArea, width, height)
        self.leftoverRect.setX(self.leftoverRect.x() + width)
        return (width, height)
    
    @validRectReturned    
    def __giveUpLeftoverSpace(self, neededArea):
        """ Sacrifice some leftover space to represent the neededARea"""
        giveUpFns = [self.__giveUpLeftoverWidth, self.__giveUpLeftoverWidth] 
        fn = giveUpFns[self.currDir]
        newRect = QRectF()
        newRect.setTopLeft(self.leftoverRect.topLeft())
        (width, height) = (self.leftoverRect.width(), self.leftoverRect.height())
        
        (width, height) = fn(neededArea, width, height)
        print "Resulting w/h %i/%i" % (width, height)
      
        if not self.leftoverRect.isValid():
            print "Failure with the following input"
            print "ParentRect %s" % repr(self.parentRect)
            print "Percentages %s" % repr(self.percs)
            assert False
        print "Leftover: %s Valid? %i" % (self.leftoverRect, self.leftoverRect.isValid())
        
        newRect.setHeight(height)
        newRect.setWidth(width)
        print "newRect H/W %lf, %lf" % (height,width)
        return newRect

        
    @validRectReturned
    def nextRect(self, percentage):
        """ Get the next rect from leftoverRect, update
            leftoverRect with whats leftover """
        self.percs.append(percentage)
        if self.isEmpty():
            raise ValueError("This guy is empty")
        neededArea = (self.parentRect.width() * self.parentRect.height()) * (percentage/100.0)
        if self.__isNeededAreaMoreThanLeftover(neededArea):
            return self.__giveUpAllRemainingArea()
        
        self.updateDirection(percentage)
        
        return self.__giveUpLeftoverSpace(neededArea)
    
    def __repr__(self):
        return "PackedRect(%s)" % repr(self.parentRect) 

    def __str__(self):
        return self.__repr__() + " Leftover(%s)" % repr(self.leftoverRect)
    
def childRects(packedRect, percentages):
    """ Given percentages and a parent packed rect,
        generate the child rects """
    for perc in percentages:
        yield packedRect.nextRect(perc)