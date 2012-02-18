from PySide.QtGui import *
from PySide.QtCore import *
import packRect
import copy


def zeroRect(rect):
    rVal = QRect()
    (height, width) = (rect.height(), rect.width())
    rVal.setX(0)
    rVal.setY(0)
    rVal.setHeight(height)
    rVal.setWidth(width)
    return rVal

def resizeRect(rect, resizeMult):
    """ Shrink a rect based on the resizeMult, ie
        if 1.2 passed in, its 1.2 times larger with
        the same center"""
    shrunkRect = QRect()
    shrunkRect = copy.deepcopy(rect)
    shrunkRect.setWidth(rect.width() * resizeMult )
    shrunkRect.setHeight(rect.height() * resizeMult )
    dx = rect.center().x() - shrunkRect.center().x() 
    dy = rect.center().y() - shrunkRect.center().y()
    shrunkRect.translate(dx, dy)
    return shrunkRect

def suppressCorners(rect, deltaX, deltaY):
    """ Bring in the corners by deltaX and deltaY
        """
    shrunkRect = QRect()
    ur = QPoint()
    lL = QPoint()
    tL = rect.topLeft()
    bR = rect.bottomRight()
    tL.setX(tL.x() + deltaX)
    tL.setY(tL.y() + deltaY)
    bR.setX(bR.x() - deltaX)
    bR.setY(bR.y() - deltaY)
    shrunkRect.setTopLeft(tL)
    shrunkRect.setBottomRight(bR)
    return shrunkRect
    

def calculateTextRect(parentRect):
    """ calculate a rectangle with the same width
        but a height 20% shorter, moving the lower
        corners up and holding the upper corners 
        the same"""
    textRect = zeroRect(parentRect)
    #scale the Y back by .2
    pt = textRect.bottomRight()
    pt.setY(pt.y() * 0.2)
    textRect.setBottomRight(pt)
    textRect.translate(parentRect.x(), parentRect.y())
    print "Rectangle: %s %s\n" % (repr(parentRect), repr(textRect))
    return textRect

class AreaPercentageItem(object):
    def __init__(self):
        object.__init__(self)
    
    def getPercentage(self):
        """ Get my percentage in the parent """
        raise NotImplementedError
    
    def getName(self):
        """ Get my name, how I should be labeled on the GUI """
        raise NotImplementedError
        
    def getChildren(self):
        """ Get a list of my children """
        raise NotImplementedError
    
    def getLeftoverPerc(self):
        raise NotImplementedError
    
class TestAreaPercentageItem(AreaPercentageItem):
    def __init__(self, perc):
        AreaPercentageItem.__init__(self)
        self.perc = perc
    
    def getPercentage(self):
        print "returning %lf" % self.perc 
        return self.perc
    
    def getName(self):
        return "Name"
    
    def getChildren(self):
        return [TestAreaPercentageItem(50), 
                TestAreaPercentageItem(10),
                TestAreaPercentageItem(10),
                TestAreaPercentageItem(5),
                TestAreaPercentageItem(3)]
    
    def getLeftoverPerc(self):
        return 22
        
        

class AreaPercentageWidget(QWidget):
    def __init__(self, parentRect, name, depth = 0, pen = None, parent = None, item = None):
        QWidget.__init__(self, parent)
        self.childAreaRects = []
        labelRect = calculateTextRect(parentRect)
        self.label = QLabel(name, self)
        self.label.setGeometry(labelRect)
        self.label.setAlignment(Qt.AlignHCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.item = item
        propUnusedSpace = 0
        print " Created %s " % parentRect   
        zeroedRect = parentRect
        print " Zeroed %s " % zeroedRect
        self.packedRect = packRect.PackedRect(zeroedRect)        
        self.currColor = 0
        self.pen = pen
        self.brush = None
        self.percIdx = 0
        self.depth = depth
        
        
    def minimumSizeHint(self):
        return self.size()
    
    #def sizeHint(self):
    #    return QSize(400,200)
        
    @Slot()
    def setShape(self, shape):
        self.shape = shape
        self.update()
    
    @Slot()
    def setPen(self, pen):
        """ Lines and outlines of shapes """
        #self.pen = pen
        #self.update()
        pass
    
    @Slot()
    def setBrush(self, brush):
        """ Brush defines fill characteristics -- color, pattern, etc """
        self.brush = brush
        self.update()
    
    @Slot()
    def setAntialiased(self, antiAliased):
        self.antialiased = antiAliased
        self.update()
        
    @Slot()
    def setTransformed(self, transformed):
        self.transformed = transformed
        self.update()
        pass
    
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.MouseButton.LeftButton:
            print "CLICKED depth = %i" % self.depth
            children = self.item.getChildren()
            if self.percIdx < len(children):
                colors = [QColor(0xff, 0, 0), QColor(0, 0xff, 0), QColor(0x00, 0x00, 0xff)]
                currPen = QPen()
                self.currColor += 1
                currPen.setWidth(5)
                currPen.setColor(colors[self.depth % 3])
                perc = children[self.percIdx].getPercentage()
                print "Getting perc %lf" % perc
                nextRect =  suppressCorners(self.packedRect.nextRect(perc), 5, 5) 
                print "nextRect %s" % str(nextRect)
                newChild = AreaPercentageWidget(parent = self,name="Hello",parentRect = zeroRect(nextRect), pen=currPen, depth=self.depth+1, item=children[self.percIdx])
                newChild.setGeometry(nextRect)
                newChild.show()
                self.percIdx += 1
        if mouseEvent.button() == Qt.MouseButton.RightButton:
            self.rotate += 1
        if mouseEvent.button() == Qt.MouseButton.MiddleButton:
            self.rotate -= 1
        self.update()
        
    def enterEvent(self, enterEvent):
        print "EnterEvent"
        filledBrush = QBrush()
        if self.pen:
            fillColor = self.pen.color()
            filledBrush.setColor(fillColor)
            filledBrush.setStyle(Qt.BrushStyle.Dense1Pattern)
            self.brush = filledBrush
            self.update()
        
    def leaveEvent(self, leaveEvent):
        self.brush = None
        self.update()
        
        
    
    def paintEvent(self, paintEvent):
        """ Paints relative to THIS windows coordinate system
            anything refering to a parents coordinate system
            must be normalized"""
        pen = QPen()
        if self.pen == None:
            pen.setColor(QColor(0xff, 0, 0))
        else:
            pen = self.pen
        
        painter = QPainter(self)
        painter.setPen(pen)
        
        if self.brush != None:
            painter.setBrush(self.brush)
        
        print "Painting %s" % str(self.packedRect.parentRect)
        
        rectToDraw = self.rect()
        rectToDraw.setWidth(rectToDraw.width()-1)
        rectToDraw.setHeight(rectToDraw.height()-1)
        
        painter.drawRect(rectToDraw)
        
        #painter.rotate(self.rotate)
        print "Painting childAreaRects %s, mywidth/height %lf, %lf " % (repr(self.childAreaRects), rectToDraw.width(), rectToDraw.height())
        for rect in self.childAreaRects:
            print "Update --- %s " % rect.rect()
            #rect.update()
        print "DONE"
            #painter.drawRect(rect)