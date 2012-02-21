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
    
class EmptyAreaPercentageItem(AreaPercentageItem):
    def __init__(self, perc,name):
        AreaPercentageItem.__init__(self)
        self.perc = perc
        self.name = name

    def getPercentage(self): 
        return self.perc
    
    def getName(self):
        return self.name
    
    def getChildren(self):
        return []
    
    def getLeftoverPerc(self):
        return 100.0

        


class AreaPercentageWidget(QWidget):
    __pallete = (QColor(0xff, 0xdf, 0x80), QColor(0x9f, 0xff, 0x80), QColor(0x80, 0xff, 0x9f))
    __reservedLabelY = 30
    __mouseOverColor = Qt.red
    __defaultPenColor = Qt.black
    __showLocalTime = True
    
    def __createDefaultPen(self):
        pen = QPen()
        adjDepth = self.absDepth
        if adjDepth == 0:
            adjDepth = 1
        pen.setWidth(2)
        pen.setColor(self.__defaultPenColor)
        return pen

        
    def __createDefaultBrush(self,parentRect):
        brush = QRadialGradient()
        brush.setRadius(parentRect.width() + parentRect.height())
        brush.setFocalPoint(parentRect.center())
        brush.setColorAt(0.0, Qt.white)
        brush.setColorAt(0.5, self.__pallete[self.absDepth % 3])
        return brush  
    
    def __createLabel(self, parentRect, text):
        labelRect = calculateTextRect(parentRect, self.__reservedLabelY)
        label = QLabel(text, self)
        label.setGeometry(labelRect)
        label.setAlignment(Qt.AlignHCenter)
        return label

    
    def __init__(self, parentRect, absDepth = 0, pen = None, brush = None, parent = None, item = None):
        QWidget.__init__(self, parent)
        self.childAreaRects = []
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.item = item
        self.label = self.__createLabel(
                    parentRect, self.item.getName()) 
        self.pen = pen
        self.brush = brush
        self.absDepth = absDepth
        if self.brush == None:
            self.brush = self.__createDefaultBrush(parentRect)
        if self.pen == None:
            self.pen = self.__createDefaultPen()
      
        try:
            shrunkInRect = moveCornersTowardCenter(parentRect, 2, self.__reservedLabelY) 
            self.packedRect = packRect.PackedRect(shrunkInRect)
            if not shrunkInRect.isEmpty():
                self.__createChildWidgets()
        except ValueError as e:
            return
        
        
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
                
    def __adjustChildRect(self, childRect):
        if childRect.width() < 0 or childRect.height() < 0:
            return None
        childRect = moveCornersTowardCenter(childRect, 5, 5)
        return childRect 
    
    def __pairChildRects(self, children):
        """ Create all child rectangles from the passed in children,
            some children may be so miniscule that a 0 percentage
            gets reported from teh item, for these no rectangle
            will be generated """
        self.__printTestVector(children)
        children = sorted(children, key=lambda child: child.getPercentage(), reverse=True)
        for child in children:
            if child.getPercentage() > 0:
                if self.packedRect.isEmpty():
                    return
                childRect = self.packedRect.nextRect(child.getPercentage())
                #assert childRect.intersected(self.rect()) == childRect
                childRect = self.__adjustChildRect(childRect)
                if childRect:
                    yield (childRect, child)
                    
    def __createChildWidget(self, parent, childRect, abDepth, item):
        newChild = AreaPercentageWidget(parent=self,
                                        parentRect=normalize(childRect),
                                        absDepth=abDepth,
                                        item=item)
        newChild.setGeometry(childRect)
        newChild.show()
        
    def __createLeftoverWidget(self, leftoverPerc):
        print "Leftover %lf" % leftoverPerc
        leftoverRect = self.packedRect.nextRect(leftoverPerc)
        leftoverRect = self.__adjustChildRect(leftoverRect)
        if leftoverRect:
            self.__createChildWidget(parent=self, 
                                     childRect=leftoverRect, 
                                     abDepth=self.absDepth+1,
                                     item=EmptyAreaPercentageItem(leftoverPerc, "local"))

    
    def __createChildWidgets(self):
        """ Generate all children widgets from child packed rects """
        print "Generating for depth %i" % self.absDepth
        if self.item == None:
            return

        children = False
        for (childRect, child ) in self.__pairChildRects(self.item.getChildren()):
            self.__createChildWidget(parent=self, 
                                     childRect=childRect, 
                                     abDepth = self.absDepth+1,
                                     item = child)
            children = True
        if self.__showLocalTime and (children):
            self.__createLeftoverWidget(self.item.getLeftoverPerc())
                
        
        
                         
    
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
            self.pen.setColor(self.__mouseOverColor)
            self.pen.setWidth(3)
        self.update()

        
    def leaveEvent(self, leaveEvent):
        self.pen = self.__createDefaultPen()
        

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
        #rectToDraw.setWidth(rectToDraw.width()-1)
        #rectToDraw.setHeight(rectToDraw.height()-1)
        
        painter.drawRect(rectToDraw)
        
