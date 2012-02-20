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
        self.renderArea = AreaPercentageWidget(QRect(0,0,640,480), item=item)
              
        self.mainLayout = QGridLayout()
        self.mainLayout.setColumnStretch(0,1)
        self.mainLayout.setColumnStretch(3,1)
        self.mainLayout.addWidget(self.renderArea, 0,0,1,4)
        self.setLayout(self.mainLayout)

        self.setWindowTitle(tr("Basic Drawing"))
        
    

if __name__ == '__main__':
    # QT parents own their childre
    app = QApplication(sys.argv)
    
    w = Window()
    app.setActiveWindow(w)
    w.show()

    app.exec_()