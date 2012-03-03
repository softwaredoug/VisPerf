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
    if textRect.height() >= minHeight:
        return textRect
    else:
        return parentRect

class AreaPercentageItem(object):
    """ This is the interface a user of AreaPercentWIdget is
        expected to implement"""
    def __init__(self):
        object.__init__(self)
    
    def getPercentage(self):
        """ Get my percentage in the parent """
        raise NotImplementedError
    
    def getName(self):
        """ Get my name, how I should be labeled on the GUI """
        raise NotImplementedError
        
    def getRtfDescription(self):
        """ Get a rich text description used for a tool-tip"""
        raise NotImplementedException
        
    def getChildren(self):
        """ Get a list of my children """
        raise NotImplementedError
    
    def getLeftoverPerc(self):
        """ Percentage not allocated to children"""
        raise NotImplementedError
    
    def getId(self):
        """ Get a number that uniquely identifies me"""
        raise NotImplementedError
    

def initialDirFromItem(item):
    """ This function looks at the item and gives a random
        direction of the item's child rects based on a
        unique property of the item thats random enough
        to make the GUI look pretty
        """
    return len(item.getName()) % 2
    
    



class AreaPercentageWidget(QWidget):
    """ A widget that draws rectangles with areas proportional
        to a portion of a whole, ie 50% would get a child rect
        half the parent's area. """
       
    __pallete = (QColor(0xff, 0xff, 0xcf), QColor(0xc7,0xff,0xff), QColor(0xff, 0xe5, 0xe5), QColor(0xcc, 0xff, 0xcc) )
    __reservedLabelY = 10
    __mouseOverColor = Qt.black
    __defaultPenColor = Qt.gray
    __childShrinkIn = (10,10)
    __maxDepth = 2
    __weakDepth = 3
    newItemSelect = Signal(int)
    
    @Slot(str)
    def __onChildSelected(self, id):
        """ Propogate my child's newItemSelect signal"""
        self.newItemSelect.emit(id)
    
    def __createDefaultPen(self):
        pen = QPen()
        pen.setColor(self.__defaultPenColor)
        if self.absDepth > self.__weakDepth:
            pen.setWidth(1)
        elif self.absDepth > self.__weakDepth / 2:
            pen.setWidth(2)
        else:
            pen.setWidth(4)
        return pen

	
    def __createDefaultBrush(self,parentRect):
        """ How this widget's area will be filled """
        if self.absDepth % 2 == 1:
            brush = QLinearGradient(parentRect.topLeft(), parentRect.topRight())
        else:
            brush = QLinearGradient(parentRect.bottomRight(), parentRect.bottomLeft())
        brush.setColorAt(0.0, Qt.white)
        brush.setColorAt(0.5, self.__pallete[self.absDepth % len(self.__pallete)])
        brush = QBrush()
        brush.setColor(self.__pallete[self.absDepth % len(self.__pallete)])
        brush.setStyle(Qt.SolidPattern)
        return brush  
    
    def __createLabel(self, parentRect, text):
        if self.absDepth > self.__weakDepth:
            self.__reservedLabelY = 0
            text = ""

        labelRect = calculateTextRect(parentRect, self.__reservedLabelY)
        label = QLabel(text, self)
        label.setGeometry(labelRect)
        label.setAlignment(Qt.AlignHCenter)
        return label

    
    def __init__(self, parentRect, absDepth = 0, parent = None, item = None):
        """ Construct the area % widget around the specified item """
        QWidget.__init__(self, parent)
        self.childAreaRects = []
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.chs = []
        self.label = None
        self.absDepth = absDepth
        self.brush = self.__createDefaultBrush(parentRect)
        self.pen = self.__createDefaultPen()
        self.setItem(item, parentRect)
        
    def minimumSizeHint(self):
        return QSize(self.packedRect.parentRect.width(), self.packedRect.parentRect.height()+50)
    
    def __printTestVector(self, children):
        """ For testing purposes, dump whats
            been drawn so far"""
        print "TESTVECTORTESTVECTOR %i children" % len(children)
        print self.packedRect.parentRect
        for child in children:
            if child.getPercentage() > 0:
                print child.getPercentage()
                
    def __adjustChildRectIn(self, childRect):
        """ Adjust a child rect in towards its center
            based on self.__childShrinkIn"""
        if childRect.width() < 0 or childRect.height() < 0:
            assert False
            return None
        rVal = moveCornersTowardCenter(childRect, 0, 0)
        (deltaX, deltaY) = self.__childShrinkIn
        if childRect.width() > deltaX * 2 and childRect.height() > deltaY * 2:
            rVal = moveCornersTowardCenter(rVal, deltaX, deltaY)
        else:
            rVal = None
        return rVal
                    
    def __createChildWidget(self, parent, childRect, abDepth, item):
        """ Create a single child widget around the item"""
        newChild = AreaPercentageWidget(parent=self,
                                        parentRect=normalize(childRect),
                                        absDepth=abDepth,
                                        item=item)
        newChild.setGeometry(childRect)
        newChild.show()
        newChild.newItemSelect.connect(self.__onChildSelected)
        return newChild
        
    
    def __createChildWidgets(self):
        """ Generate all children widgets from child packed rects """
        if self.item == None:
            return
        
        if self.absDepth > self.__maxDepth:
            return

        for (child, childRect) in self.packedRect:
            childRect = self.__adjustChildRectIn(childRect)
            if childRect:
                self.__createChildWidget(parent=self, 
                                         childRect=childRect, 
                                         abDepth = self.absDepth+1,
                                         item = child)     
        
    def setItem(self, item, parentRect):        
        """ Initialize me around the specified item """             
        self.item = item
        self.setToolTip(item.getRtfDescription())
        if self.label:
            del self.label
        for ch in self.chs:
            del ch
        self.label = self.__createLabel(
                    parentRect, self.item.getName())
        # Pick a deterministic
        initialDir = initialDirFromItem(self.item)
        if parentRect.width() > 4 and parentRect.height() > self.__reservedLabelY*2:
            shrunkInRect = moveCornersTowardCenter(parentRect, 0, self.__reservedLabelY) 
            self.packedRect = packRect.PackedRect(shrunkInRect, item.getChildren(), initialDir)
            if not shrunkInRect.isEmpty():
                self.__createChildWidgets()
        else:
            self.packedRect = packRect.emptyPackedRect
        self.update()      

    def mousePressEvent(self, mouseEvent):
        """ If I'm clicked, indicate the new selection"""
        if mouseEvent.button() == Qt.MouseButton.LeftButton:
            self.newItemSelect.emit(self.item.getId())
        
    def enterEvent(self, enterEvent):
        """ Upon a mouse entering, highlight this widget"""
        self.setToolTip(self.item.getRtfDescription())
        if self.pen != None:
            self.pen.setColor(self.__mouseOverColor)
            self.pen.setWidth(3)
        self.update()

        
    def leaveEvent(self, leaveEvent):
        """ Upon a mouse entering, unhighlight this widget"""
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
        painter.setBackgroundMode(Qt.TransparentMode)
        
        if self.brush != None:
            painter.setBrush(self.brush)
        
        
        rectToDraw = self.rect()
        if rectToDraw:
            painter.drawRect(rectToDraw)
        #rectToDraw.setWidth(rectToDraw.width()-1)
        #rectToDraw.setHeight(rectToDraw.height()-1)
        
        
        
