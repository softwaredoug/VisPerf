from PySide.QtGui import *
from PySide.QtCore import *
import packRect
from rectUtils import *
import copy
 

def calculateTextRect(parentRect, minHeight):
    """ calculate a rectangle with the same width
        but a height 20% shorter, moving the lower
        corners up and holding the upper corners 
        the same"""
    textRect = normalize(parentRect)
    #scale the Y back by .2
    pt = textRect.bottomRight()
    pt.setY(pt.y() * 0.2)
    textRect.setBottomRight(pt)
    textRect.translate(parentRect.x(), parentRect.y())
    print "Rectangle: %s %s\n" % (repr(parentRect), repr(textRect))
    if textRect.height() >= minHeight:
        return textRect
    else:
        return parentRect

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
                TestAreaPercentageItem(20),
                TestAreaPercentageItem(10),
                TestAreaPercentageItem(5)]
    
    def getLeftoverPerc(self):
        return 0.1
        
        

class AreaPercentageWidget(QWidget):
    def __init__(self, parentRect, absDepth = 0, pen = None, brush = None, parent = None, item = None):
        QWidget.__init__(self, parent)
        self.childAreaRects = []
        labelRect = calculateTextRect(parentRect, 50)
        self.label = QLabel(item.getName(), self)
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
        self.brush = brush
        self.percIdx = 0
        self.absDepth = absDepth
        if self.absDepth < 2:
            self.__createChildWidgets()
        
        
    def minimumSizeHint(self):
        return self.size()
    
    #def sizeHint(self):
    #    return QSize(400,200)
    def __printTestVector(self, children):
        print "TESTVECTORTESTVECTOR"
        print self.packedRect.parentRect
        for child in children:
            if child.getPercentage() > 0:
                print child.getPercentage()
    
    def __pairChildRects(self, children):
        """ Create all child rectangles from the passed in children,
            some children may be so miniscule that a 0 percentage
            gets reported from teh item, for these no rectangle
            will be generated """
        self.__printTestVector(children)
        for child in children:
            if child.getPercentage() > 0:
                if self.packedRect.isEmpty():
                    return
                childRect = self.packedRect.nextRect(child.getPercentage())
                (alwaysShrinkX, alwaysShrinkY) = (10,30)
                if childRect.width() < (alwaysShrinkX * 2):
                    alwaysShrinkX = 0
                if childRect.height() < (alwaysShrinkY * 2):
                    alwaysShrinkY = 0
                childRect = moveCornersTowardCenter(childRect, alwaysShrinkX, alwaysShrinkY) 
                assert childRect.intersected(self.packedRect.parentRect) == childRect

                yield (childRect, child)       
    
    def __createChildWidgets(self):
        """ Generate all children widgets from child packed rects """
        print "Generating for depth %i" % self.absDepth
        colors = [QColor(0xff, 0, 0), QColor(0, 0xff, 0), QColor(0x00, 0x00, 0xff)]
        currPen = QPen()
        self.currColor += 1
        currPen.setWidth(1)
        currPen.setColor(Qt.white)

        for (childRect, child ) in self.__pairChildRects(self.item.getChildren()):
            brush = QRadialGradient(1,self.height() /2,self.rect().height()*2)
            brush.setColorAt(0.0, Qt.white)
            brush.setColorAt(0.5, colors[self.absDepth % 3])
            newChild = AreaPercentageWidget(parent = self,
                                            parentRect = normalize(childRect),
                                            pen=currPen,
                                            brush = brush,
                                            absDepth=self.absDepth+1,
                                            item=child)
            newChild.setGeometry(childRect)
            newChild.show()
                         
    
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.MouseButton.LeftButton:
            print "CLICKED name = %s geom %s " % (self.label.text(), self.geometry())
            print "Children:"
            for child in self.item.getChildren():
                print "Name/Perc %s/%lf" % (child.getName(), child.getPercentage())
            #self.__createChildWidgets()
        self.update()
        
    def enterEvent(self, enterEvent):
        if self.pen != None:
            self.pen.setColor(Qt.black)
            self.pen.setWidth(3)

        
    def leaveEvent(self, leaveEvent):
        if self.pen != None:
            self.pen.setColor(Qt.white)
            self.pen.setWidth(1)
            self.parentWidget().leaveEvent(leaveEvent)
        

        #self.brush = None
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
        
        #print "Painting %s" % str(self.packedRect.parentRect)
        
        rectToDraw = self.rect()
        rectToDraw.setWidth(rectToDraw.width()-1)
        rectToDraw.setHeight(rectToDraw.height()-1)
        
        painter.drawRect(rectToDraw)
        
