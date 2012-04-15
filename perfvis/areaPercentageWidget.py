from PySide.QtGui import *
from PySide.QtCore import *
import packRect
from rectUtils import *
import copy
from callerCalleePercentageItem import sortedByPerc, CallerCalleePercentageItem
 

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
    
def createFunctionLabel(function):
    baseName = function.getName()
    overallPerc = function.getOverallPerc()
    rVal =  "<" + str(function.getLocalPercentage())[:4] + "> (" + str(overallPerc)[:4] + ")" + baseName
    return rVal[-100:]
    


class AreaPercentageWidget(QWidget):
    """ A widget that draws rectangles with areas proportional
        to a portion of a whole, ie 50% would get a child rect
        half the parent's area. """
    __grid = QRect(0,0,20,10)
    __pallete = (QColor(0xff, 0xff, 0xcf), QColor(0xc7,0xff,0xff), QColor(0xff, 0xe5, 0xe5), QColor(0xcc, 0xff, 0xcc) )
    __reservedLabelY = 10
    __mouseOverColor = Qt.black
    __defaultPenColor = Qt.gray
    __childTrimIn = (5,5)
    __postTrimDontShow = (5,5)
    __weakDepth = 3
    newRootFunctionSelected = Signal(int)
    
    @Slot(str)
    def __onChildSelected(self, functionAddr):
        """ Propogate my child's newRootFunctionSelected signal"""
        self.newRootFunctionSelected.emit(functionAddr)
    
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

    
    def __init__(self, parentRect, absDepth = 0, maxAbsDepth = 0, parent = None, rootFunction = None):
        """ Construct the area % widget around the specified rootFunction """
        QWidget.__init__(self, parent)
        self.childAreaRects = []
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.chs = []
        self.label = None
        self.absDepth = absDepth
        self.maxAbsDepth = maxAbsDepth
        self.brush = self.__createDefaultBrush(parentRect)
        self.pen = self.__createDefaultPen()
        self.setRootFunction(rootFunction, parentRect)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        
    def minimumSizeHint(self):
        return QSize(self.parentRect.width(), self.parentRect.height()+50)
    
    def __printTestVector(self, children):
        """ For testing purposes, dump whats
            been drawn so far"""
        print "TESTVECTORTESTVECTOR %i children" % len(children)
        print self.packedRect.parentRect
        for child in children:
            if child.getLocalPercentage() > 0:
                print child.getLocalPercentage()
                
    def __adjustChildRectIn(self, childRect):
        """ Adjust a child rect in towards its center
            based on self.__childTrimIn"""
        if childRect.width() < 0 or childRect.height() < 0:
            assert False
            return None
        (postTrimDontShowW, postTrimDontShowH) =  (AreaPercentageWidget.__postTrimDontShow[0],
                                           AreaPercentageWidget.__postTrimDontShow[1])

        rVal = moveCornersTowardCenter(childRect, 0, 0)
        (deltaX, deltaY) = self.__childTrimIn
        if childRect.width() > deltaX * 2 and childRect.height() > deltaY * 2:
            rVal = moveCornersTowardCenter(rVal, deltaX, deltaY)
        else:
            return None
        
        if rVal.width() < postTrimDontShowW or rVal.height() < postTrimDontShowH:
            return None    
            
        return rVal
    
    def __scaleToGeom(self, rect):
        geom = QRectF(self.parentRect)
        xScale = geom.width() / self.__grid.width()
        yScale = geom.height() / self.__grid.height()
        
        return QRect(rect.x() * xScale, rect.y() * yScale, rect.width() * xScale, rect.height() * yScale)

                    
    def __createChildWidget(self, parent, childRect, absDepth, maxAbsDepth, childFunction):
        """ Create a single child widget around the childFunction"""
        newChild = AreaPercentageWidget(parent=self,
                                        parentRect=normalize(childRect),
                                        absDepth=absDepth,
                                        maxAbsDepth=maxAbsDepth,
                                        rootFunction=childFunction)
        newChild.setGeometry(childRect)
        newChild.show()
        newChild.newRootFunctionSelected.connect(self.__onChildSelected)
        return newChild
        
    
    def __createChildWidgets(self):
        """ Generate all children widgets from child packed rects """
        if self.rootFunction == None:
            return
        
        if self.absDepth >= self.maxAbsDepth:
            return

        for (child, childRect) in self.packedRect:
            scaledRect = self.__scaleToGeom(childRect)
            if not scaledRect.isEmpty():
                scaledRect = self.__adjustChildRectIn(scaledRect)
                if scaledRect:
                    self.__createChildWidget(parent=self, 
                                             childRect=scaledRect, 
                                             absDepth = self.absDepth+1,
                                             maxAbsDepth=self.maxAbsDepth,
                                             childFunction = child)     
        
    def setRootFunction(self, rootFunction, parentRect):        
        """ Initialize me around the specified rootFunction """             
        self.rootFunction = rootFunction
        self.setToolTip(rootFunction.getFullPerfDescription(rtf=True))
        if self.label:
            del self.label
        for ch in self.chs:
            del ch
        self.label = self.__createLabel(
                    parentRect, createFunctionLabel(self.rootFunction))
        if parentRect.width() > 4 and parentRect.height() > self.__reservedLabelY*2:
            initHeight = parentRect.y()
            shrunkInRect = moveCornersTowardCenter(parentRect, 0, self.__reservedLabelY+50)
            self.parentRect = parentRect
            print "shrunk in %i to %i" % (initHeight, shrunkInRect.y())
            self.packedRect = packRect.PackedRect(self.__grid, rootFunction.createCallees())
            if not shrunkInRect.isEmpty():
                self.__createChildWidgets()
        else:
            self.packedRect = packRect.emptyPackedRect
        self.update()      

    def mousePressEvent(self, mouseEvent):
        """ If I'm clicked, indicate the new selection"""
        if mouseEvent.button() == Qt.MouseButton.LeftButton:
            self.newRootFunctionSelected.emit(self.rootFunction.getAddress())
        else:
            QWidget.mousePressEvent(self, mouseEvent)
        
    def enterEvent(self, enterEvent):
        """ Upon a mouse entering, highlight this widget"""
        self.setToolTip(self.rootFunction.getFullPerfDescription(rtf=True))
        if self.pen != None:
            self.pen.setColor(self.__mouseOverColor)
            self.pen.setWidth(3)
        self.update()

        
    def leaveEvent(self, leaveEvent):
        """ Upon a mouse entering, unhighlight this widget"""
        self.pen = self.__createDefaultPen()
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
            
    
    def __createActionCallbackToSelectFunction(self, selectedFunctionId):
        """ Create a callback to select selectedFunctionId for view """
        @Slot(bool)
        def actionSelectedSlot(checked=False):
            self.newRootFunctionSelected.emit(selectedFunctionId)
        return actionSelectedSlot
    
    @Slot(bool)
    def __copyPerfReportToClipboard(self, checked=False):
        """ Copy whats presented in the tooltip to the clipboard"""
        clipboard = QApplication.clipboard()
        fullDescMime = QMimeData()
        fullDescMime.setHtml(self.rootFunction.getFullPerfDescription(rtf=True))
        fullDescMime.setText(self.rootFunction.getFullPerfDescription(rtf=False))
        clipboard.setMimeData(fullDescMime)
    
    def __createActionForFunction(self, function):
        """ Create a menu action for the passed in area percentage
            rootFunction"""
        action = QAction(unicode(createFunctionLabel(function)), self)
        action.triggered.connect(self.__createActionCallbackToSelectFunction(function.getAddress()))
        return action

    @Slot(QPoint)
    def showContextMenu(self, pos):
        """ Draw a custom context menu for this 
            area percentage widget, all the work of 
            the actions is done via callbacks """
        globalPos = self.mapToGlobal(pos)
        
        copyReport = QAction("Copy Perf Report", self)
        copyReport.triggered.connect(self.__copyPerfReportToClipboard)
        
        # Actions to select each callee, sorted by %
        childActions = [self.__createActionForFunction(callee) for callee in
                         sortedByPerc(self.rootFunction.createCallees())]
        # Actions to select each caller, sorted by %
        parentActions = [self.__createActionForFunction(caller) for caller in
                          sortedByPerc(self.rootFunction.createCallers())]
        
        goToChild = QMenu("Go To Child")
        goToChild.addActions(childActions)
        
        goToParent = QMenu("Go To Parent")
        goToParent.addActions(parentActions)       
        
        myMenu = QMenu()
        myMenu.addAction(copyReport)
        myMenu.addMenu(goToChild)
        myMenu.addMenu(goToParent)
        myMenu.exec_(globalPos)
                
        
