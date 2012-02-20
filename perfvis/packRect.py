
from PySide.QtCore import QRect
from rectUtils import validRectReturned

class Direction:
    Horizontal = False
    Vertical = True
    
    @staticmethod
    def flip(direction):
        return not direction
  

class PackedRect:
    """ Given p and a starting rect, draw
        a subrectangle that takes p% of the
        area of the starting rect. Repeat for p1,p2...
        as long as there continues to be room in the parent rect"""  
    
    def __init__(self, parentRect):
        self.parentRect = self.leftoverRect = QRect()
        self.parentRect = parentRect
        print "PackedRect Created with %s" % str(parentRect)
        self.reset()
        
    def reset(self):
        import copy
        self.lastFlipPercentage = 100
        self.currDir = Direction.Horizontal
        self.leftoverRect = copy.deepcopy(self.parentRect)
        
    def updateDirection(self, currPercentage):
        magnitude = 0
        if currPercentage > self.lastFlipPercentage:
            magnitude = currPercentage / self.lastFlipPercentage
        else:
            magnitude = self.lastFlipPercentage / currPercentage
        if magnitude > 3.0:
            print "Flip..."
            self.currDir = Direction.flip(self.currDir)
            self.lastFlipPercentage = currPercentage
            
    def isEmpty(self):
        return self.leftoverRect.isEmpty()
            
    @validRectReturned
    def __giveUpAllRemainingArea(self):
        """ Return all remaining leftover space and empty
            the leftover rect"""
        assert not self.leftoverRect.isEmpty()
        print "Giving up remaining..."
        remaining = QRect(self.leftoverRect)
        self.leftoverRect.setWidth(-1)
        self.leftoverRect.setHeight(-1)
        assert self.leftoverRect.isEmpty()
        return remaining
   
    @validRectReturned 
    def __giveUpLeftoverHeight(self, neededArea):
        """ Sacrifice height from the leftover rect for the needed area"""
        newRect = QRect()
        newRect.setTopLeft(self.leftoverRect.topLeft())

        # a = width * height we know which a we want, so we 
        # need to calculate a height to satisfy the neededArea

        (width, height) = (self.leftoverRect.width(), self.leftoverRect.height())
        height = neededArea / width
        print "Vertical..., na %lf width %lf height %lf" % (neededArea, width, height)
        if height < 1:
            height = 1
        if self.leftoverRect.height() <= height:
            return self.__giveUpAllRemainingArea()
        self.leftoverRect.setY(self.leftoverRect.y() + height)
        assert self.leftoverRect.isValid()
        print "Leftover: %s Valid? %i" % (self.leftoverRect, self.leftoverRect.isValid())
        print "newRect H/W %lf, %lf" % (height,width)
        
        newRect.setHeight(height)
        newRect.setWidth(width)
        return newRect
    
    @validRectReturned
    def __giveUpLeftoverWidth(self, neededArea):
        """ Sacrifice width from the leftover rect for the needed area"""
        newRect = QRect()
        newRect.setTopLeft(self.leftoverRect.topLeft())
        
       
        (width, height) = (self.leftoverRect.width(), self.leftoverRect.height())
        width = neededArea / height
        print "Horizontal..., na %lf width %lf height %lf" % (neededArea, width, height)
        if width < 1:
            width = 1
        if self.leftoverRect.width() <= width:
            return self.__giveUpAllRemainingArea()
        self.leftoverRect.setX(self.leftoverRect.x() + width)
        assert self.leftoverRect.isValid()
        print "Leftover: %s Valid? %i" % (self.leftoverRect, self.leftoverRect.isValid())
        print "newRect H/W %lf, %lf" % (height,width)

        newRect.setHeight(height)
        newRect.setWidth(width)
        return newRect

        
    @validRectReturned
    def nextRect(self, percentage):
        """ Get the next rect from leftoverRect, update
            leftoverRect with whats leftover """
        neededArea = (self.parentRect.width() * self.parentRect.height()) * (percentage/100.0)
        leftoverArea = self.leftoverRect.width() * self.leftoverRect.height()
        if neededArea > leftoverArea:
            raise ValueError("Insufficient area, needed %lf, available %lf" % (neededArea, leftoverArea))
        
        self.updateDirection(percentage)
        
        
        # Take the width of the current leftoverRect
        # but adjust
        if self.currDir == Direction.Horizontal:
            # a = width * height we know which a we want, so we 
            # need to calculate a width to satisfy the neededArea
            return self.__giveUpLeftoverWidth(neededArea)
        elif self.currDir == Direction.Vertical:
            return self.__giveUpLeftoverHeight(neededArea)
        else:
            print "ERROR -- %s" % str(self.currDir)
            assert False
    
    def __repr__(self):
        return "PackedRect(%s)" % repr(self.parentRect) 

    def __str__(self):
        return self.__repr__() + " Leftover(%s)" % repr(self.leftoverRect)
    
def childRects(packedRect, percentages):
    """ Given percentages and a parent packed rect,
        generate the child rects """
    for perc in percentages:
        yield packedRect.nextRect(perc)