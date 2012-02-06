
from PySide import QtCore

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
        self.parentRect = self.leftoverRect = QtCore.QRect()
        self.parentRect = parentRect
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
        

    def nextRect(self, percentage):
        """ Get the next rect from leftoverRect, update
            leftoverRect with whats leftover """
        neededArea = (self.parentRect.width() * self.parentRect.height()) * (percentage/100.0)
        leftoverArea = self.leftoverRect.width() * self.leftoverRect.height()
        if neededArea > leftoverArea:
            raise ValueError("Insufficient area, needed %lf, available %lf" % (neededArea, leftoverArea))
        
        self.updateDirection(percentage)
        
        newRect = QtCore.QRect()
        newRect.setTopLeft(self.leftoverRect.topLeft())
        
        # Take the width of the current leftoverRect
        # but adjust
        (width, height) = (self.leftoverRect.width(), self.leftoverRect.height())
        if self.currDir == Direction.Horizontal:
            # a = width * height we know which a we want, so we 
            # need to calculate a width to satisfy the neededArea
            width = neededArea / height
            self.leftoverRect.setX(self.leftoverRect.x() + width)
            print "Horizontal..., na %lf width %lf height %lf" % (neededArea, width, height)
        elif self.currDir == Direction.Vertical:
            # a = width * height we know which a we want, so we 
            # need to calculate a height to satisfy the neededArea
            height = neededArea / width
            self.leftoverRect.setY(self.leftoverRect.y() + height)
            print "Vertical..., na %lf width %lf height %lf" % (neededArea, width, height)
        else:
            print "ERROR -- %s" % str(self.currDir)
        newRect.setHeight(height)
        newRect.setWidth(width)
        return newRect