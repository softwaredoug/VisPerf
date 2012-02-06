'''
Created on Feb 1, 2012

@author: Doug
'''
from PySide import QtGui, QtCore
import sys
import packRect
import copy
def tr(str):
    return str

def zeroRect(rect):
    (height, width) = (rect.height(), rect.width())
    rect.setX(0)
    rect.setY(0)
    rect.setHeight(height)
    rect.setWidth(width)

class AreaPercentageWidget(QtGui.QWidget):
    
    def __init__(self, parentRect, depth = 0, pen = None, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.childAreaRects = []
        self.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.percentages = [30,20,7,7,6,5,5,5,5,5,5,5,5,5,2,2,2,0.1,0.1]
        print " Created %s " % parentRect
        self.setGeometry(parentRect)   
        zeroedRect = copy.deepcopy(parentRect)   
        zeroRect(zeroedRect)
        self.packedRect = packRect.PackedRect(zeroedRect)        
        self.currColor = 0
        self.pen = pen
        self.percIdx = 0
        self.depth = depth
        
        
    def minimumSizeHint(self):
        return self.size()
    
    #def sizeHint(self):
    #    return QtCore.QSize(400,200)
        
    @QtCore.Slot()
    def setShape(self, shape):
        self.shape = shape
        self.update()
    
    @QtCore.Slot()
    def setPen(self, pen):
        """ Lines and outlines of shapes """
        #self.pen = pen
        #self.update()
        pass
    
    @QtCore.Slot()
    def setBrush(self, brush):
        """ Brush defines fill characteristics -- color, pattern, etc """
        self.brush = brush
        self.update()
    
    @QtCore.Slot()
    def setAntialiased(self, antiAliased):
        self.antialiased = antiAliased
        self.update()
        
    @QtCore.Slot()
    def setTransformed(self, transformed):
        self.transformed = transformed
        self.update()
        pass
    
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == QtCore.Qt.MouseButton.LeftButton:
            print "CLICKED depth = %i" % self.depth
            if self.percIdx < len(self.percentages):
                colors = [QtGui.QColor(0xff, 0, 0), QtGui.QColor(0, 0xff, 0), QtGui.QColor(0x00, 0x00, 0xff)]
                currPen = QtGui.QPen()
                self.currColor += 1
                currPen.setWidth(5)
                currPen.setColor(colors[self.depth % 3])
                perc = self.percentages[self.percIdx]
                nextRect = self.packedRect.nextRect(perc)
                newChild = AreaPercentageWidget(parent = self,parentRect = nextRect, pen=currPen, depth=self.depth+1)
                newChild.show()
                self.percIdx += 1
        if mouseEvent.button() == QtCore.Qt.MouseButton.RightButton:
            self.rotate += 1
        if mouseEvent.button() == QtCore.Qt.MouseButton.MiddleButton:
            self.rotate -= 1
        self.update()
        
    
    def paintEvent(self, paintEvent):
        """ Paints relative to THIS windows coordinate system
            anything refering to a parents coordinate system
            must be normalized"""
        import copy
        pen = QtGui.QPen()
        if self.pen == None:
            pen.setColor(QtGui.QColor(0xff, 0, 0))
        else:
            pen = self.pen
        
        painter = QtGui.QPainter(self)
        painter.setPen(pen)
        
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
            
      

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.renderArea = AreaPercentageWidget(QtCore.QRect(0,0,640,480))
        
        self.shapeLabel = QtGui.QLabel("&Shape")
        
        self.penWidthSpinBox = QtGui.QSpinBox()
        self.penWidthSpinBox.setRange(0,20)
        self.penWidthSpinBox.setSpecialValueText(tr("0 (cosmetic pen)"))
        self.penWidthLabel = QtGui.QLabel(tr("Pen &Width"))
        self.penWidthLabel.setBuddy(self.penWidthSpinBox)
        
        self.penStyleComboBox = QtGui.QComboBox()
        self.penStyleComboBox.addItem(tr("Solid"), QtCore.Qt.SolidLine)
        self.penStyleComboBox.addItem(tr("Dash"), QtCore.Qt.DashLine)
        self.penSyleLable = QtGui.QLabel(tr("&Pen Style"))
        self.penSyleLable.setBuddy(self.penStyleComboBox)
        
        self.penCapComboBox = QtGui.QComboBox()
        self.penCapComboBox.addItem(tr("Flat"), QtCore.Qt.FlatCap)
        self.penCapComboBox.addItem(tr("Square"), QtCore.Qt.SquareCap)
        self.penCapComboBox.addItem(tr("Round"), QtCore.Qt.RoundCap)
        self.penCapLabel = QtGui.QLabel(tr("Pen &Cap"))
        self.penCapLabel.setBuddy(self.penCapLabel)
        
        self.penJoinComboBox = QtGui.QComboBox()
        self.penJoinComboBox.addItem(tr("Miter"), QtCore.Qt.MiterJoin)
        self.penJoinComboBox.addItem(tr("Bevel"), QtCore.Qt.BevelJoin)
        self.penJoinComboBox.addItem(tr("Round"), QtCore.Qt.RoundJoin)
        self.penJoinLabel = QtGui.QLabel("Pen &Join")
        self.penJoinLabel.setBuddy(self.penJoinLabel)
        
        self.brushStyleComboBox = QtGui.QComboBox()
        self.brushStyleComboBox.addItem(tr("Linear Gradient"), QtCore.Qt.LinearGradientPattern)
        self.brushStyleComboBox.addItem(tr("Radial Gradient"), QtCore.Qt.RadialGradientPattern)
        self.brushStyleComboBox.addItem(tr("None"), QtCore.Qt.NoBrush)
        self.brushStyleLabel = QtGui.QLabel()
        self.brushStyleLabel.setBuddy(self.brushStyleComboBox)
        
        self.otherOptionsLabel = QtGui.QLabel(tr("Other Options:"))
        self.antialiasingCheckbox = QtGui.QCheckBox(tr("&Antialiasing"))
        self.transformationsCheckbox = QtGui.QCheckBox(tr("&Transformations"))
        
        #Con
        
        self.mainLayout = QtGui.QGridLayout()
        self.mainLayout.setColumnStretch(0,1)
        self.mainLayout.setColumnStretch(3,1)
        self.mainLayout.addWidget(self.renderArea, 0,0,1,4)
        self.mainLayout.setRowMinimumHeight(1,6)
        self.mainLayout.addWidget(self.shapeLabel, 2,1, QtCore.Qt.AlignRight)
        self.mainLayout.addWidget(self.penWidthLabel, 3, 1, QtCore.Qt.AlignRight)
        self.mainLayout.addWidget(self.penWidthSpinBox, 3, 2)
        self.mainLayout.addWidget(self.penSyleLable, 3,1, QtCore.Qt.AlignRight)
        self.mainLayout.addWidget(self.penStyleComboBox, 4, 2)
        self.mainLayout.addWidget(self.penCapLabel, 5, 1, QtCore.Qt.AlignRight)
        self.mainLayout.addWidget(self.penCapComboBox, 5, 2)
        self.mainLayout.addWidget(self.penJoinLabel, 6, 1, QtCore.Qt.AlignRight)
        self.mainLayout.addWidget(self.penJoinComboBox, 6, 2)
        self.mainLayout.addWidget(self.brushStyleLabel, 7, 1, QtCore.Qt.AlignRight)
        self.mainLayout.addWidget(self.brushStyleComboBox, 7, 2)
        self.mainLayout.setRowMinimumHeight(8, 6)
        self.mainLayout.addWidget(self.otherOptionsLabel, 9, 1, QtCore.Qt.AlignRight)
        self.mainLayout.addWidget(self.antialiasingCheckbox, 9, 2)
        self.mainLayout.addWidget(self.transformationsCheckbox, 10, 2)
        self.setLayout(self.mainLayout)
        
        self.penChanged()
        self.brushChanged()
        self.antialiasingCheckbox.setChecked(True)
        self.setWindowTitle(tr("Basic Drawing"))
        
        
    def penChanged(self):
        width =self.penWidthSpinBox.value()
        style = QtCore.Qt.PenStyle( self.penStyleComboBox.currentIndex() )
        cap = QtCore.Qt.PenCapStyle( self.penCapComboBox.currentIndex())
        join = QtCore.Qt.PenJoinStyle( self.penJoinComboBox.currentIndex() )
        pen = QtGui.QPen(QtCore.Qt.blue, width, style, cap, join)
        self.renderArea.setPen( pen)
    
    def brushChanged(self):
        style = QtCore.Qt.BrushStyle( self.brushStyleComboBox.itemData( self.brushStyleComboBox.currentIndex()))
        linearGradient = QtGui.QLinearGradient(0, 0, 100, 100)
        linearGradient.setColorAt(0.0, QtCore.Qt.white)
        linearGradient.setColorAt(0.2, QtCore.Qt.green)
        linearGradient.setColorAt(1.0, QtCore.Qt.black)
        self.renderArea.setBrush(linearGradient)
        
    

if __name__ == '__main__':
    # QT parents own their childre
    app = QtGui.QApplication(sys.argv)
    
    w = Window()
    app.setActiveWindow(w)
    w.show()

    app.exec_()