'''
Created on Feb 1, 2012

@author: Doug
'''
from PySide.QtGui import *
from PySide.QtCore import *
import sys
from areaPercentageWidget import AreaPercentageWidget, TestAreaPercentageItem
from callerCalleePercentageItem import CallerCalleePercentageItem
from callercallee.report import loadReport
def tr(str):
    return str


    
      

class Window(QWidget):
    def createAreaPercWidget(self, name):
        item = CallerCalleePercentageItem(self.report, name, 100.0)
        #item = TestAreaPercentageItem(100.0)
        geom = QRect(0,0,1280,1000)
        self.renderArea = AreaPercentageWidget(geom, item=item)
        self.renderArea.setGeometry(geom)
        self.mainLayout.addWidget(self.renderArea)
              
        self.renderArea.newItemSelect.connect(self.onNewItem)
        self.renderArea.show()

    
    def __init__(self):
        QWidget.__init__(self)
        self.report = loadReport(sys.argv[1])
        self.setWindowTitle(tr("Basic Drawing"))
        self.mainLayout = QVBoxLayout()
        self.createAreaPercWidget("")
        self.setLayout(self.mainLayout)

    
    @Slot(str)
    def onNewItem(self, selectedItemName):
        print "ON NEW ITEM %s" % selectedItemName
        self.renderArea.deleteLater()
        self.mainLayout.removeWidget(self.renderArea)
        self.createAreaPercWidget(selectedItemName)
    

if __name__ == '__main__':
    # QT parents own their childre
    app = QApplication(sys.argv)
    
    w = Window()
    app.setActiveWindow(w)
    w.show()

    app.exec_()