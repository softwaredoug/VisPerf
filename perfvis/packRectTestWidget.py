from PySide.QtCore import *
from PySide.QtGui import *

from packRect import PackedRect, TestItem

class PackedRectTestWidget(QWidget):
    __grid = QRect(0,0,20,10)
    __pallete = (QColor(0xff, 0xff, 0xcf), QColor(0xc7,0xff,0xff), QColor(0xff, 0xe5, 0xe5), QColor(0xcc, 0xff, 0xcc) )
    """ A widget simply existing for useful visual testing of
        what the PackedRect class is putting out """
    def __init__(self, items, geom):
        QWidget.__init__(self)
        self.setGeometry(geom)
        self.packRect = PackedRect(self.__grid, items)
        self.rectsToDraw = []
        self.rectLabels = []
        self.pen = QPen()
        self.pen.setColor(QColor(0xff, 0, 0))
        
    def __scaleToParentRect(self, rect):
        geom = QRectF(self.geometry())
        xScale = geom.width() / self.__grid.width()
        yScale = geom.height() / self.__grid.height()
        
        return QRect(rect.x() * xScale, rect.y() * yScale, rect.width() * xScale, rect.height() * yScale)
        
   
    def mousePressEvent(self, mouseEvent):
        """ If I'm clicked, indicate the new selection"""
        if mouseEvent.button() == Qt.MouseButton.LeftButton:
            try:
                (item, rect) = self.packRect.next()
                scaledRect = self.__scaleToParentRect(rect)
                self.rectsToDraw.append(scaledRect)
                newLabel = QLabel(self)
                newLabel.setText(str(item.getLocalPercentage())+"%")
                newLabel.setGeometry(scaledRect)
                newLabel.show()
                self.rectLabels.append(newLabel)
                self.update()
            except StopIteration:
                pass
            
    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.setBackgroundMode(Qt.TransparentMode)
        
        brush = QBrush()      
        
        painter.drawRect(self.geometry())
        print "GOING TO DRAW..."
        print self.rectsToDraw
        for (iterNum, rect) in enumerate(self.rectsToDraw):
            brush.setColor(self.__pallete[iterNum % len(self.__pallete)])
            brush.setStyle(Qt.SolidPattern)       
            
            painter.setBrush(brush)
            painter.drawRect(rect)

app = QApplication([])  

def testPackedRect(percentages, geom=QRect(0,0,1024,768)):
    w = PackedRectTestWidget([TestItem(perc) for perc in percentages], geom)
    app.setActiveWindow(w)
    w.show()

    app.exec_()
