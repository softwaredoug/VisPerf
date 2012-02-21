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
    def __init__(self):
        QWidget.__init__(self)
        report = loadReport(sys.argv[1])
        item = CallerCalleePercentageItem(report, "_wmainCRTStartup", 100.0)
        #item = TestAreaPercentageItem(100.0)
        geom = QRect(0,0,1024,780)
        self.renderArea = AreaPercentageWidget(geom, item=item)
        self.renderArea.setGeometry(geom)
              
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.renderArea)
        self.setLayout(self.mainLayout)

        self.setWindowTitle(tr("Basic Drawing"))
        
    

if __name__ == '__main__':
    # QT parents own their childre
    app = QApplication(sys.argv)
    
    w = Window()
    app.setActiveWindow(w)
    w.show()

    app.exec_()