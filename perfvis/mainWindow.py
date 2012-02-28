'''
Created on Feb 1, 2012

@author: Doug
'''
from PySide.QtGui import *
from PySide.QtCore import *
from exploreWidget import ExploreControls
import sys
from areaPercentageWidget import AreaPercentageWidget
from callerCalleePercentageItem import CallerCalleePercentageItem
from callercallee.report import loadReport
def tr(str):
    return str




    
      

class Window(QWidget):
    def createAreaPercWidget(self):
        item = CallerCalleePercentageItem(self.report, self.selectedAddr, 100.0)
        #item = TestAreaPercentageItem(100.0)
        geom = QRect(0,0,1024,780)
        self.renderArea = AreaPercentageWidget(geom, item=item)

        self.mainLayout.addWidget(self.renderArea)
              
        self.renderArea.newItemSelect.connect(self.onNewItemSelected)
        #self.renderArea.show()
        
    def setupControls(self):
        sortedVals = sorted(self.report.getAllRecords().values(),
                             key = lambda rec: rec.getRoot().getElapsedIncl(),
                             reverse = True)
        self.selectedAddr = sortedVals[0].getRoot().getFunctionAddr()
        rootFuncs = [(rec.getRoot().getFunctionAddr(), rec.getRoot().getFunctionName())
                      for rec in sortedVals]
            
        self.explWidget = ExploreControls(parent=self, funcs=rootFuncs)
        self.mainLayout.addWidget(self.explWidget)
        self.explWidget.newItemSelect.connect(self.onNewItemSelected)
        #self.explWidget.show()

    
    def __init__(self):
        QWidget.__init__(self)
        self.report = loadReport(sys.argv[1])
        self.setWindowTitle(tr("Basic Drawing"))
        self.mainLayout = QVBoxLayout()
        self.setupControls()
        self.createAreaPercWidget()
        
        self.setLayout(self.mainLayout)

    
    @Slot(int)
    def onNewItemSelected(self, selectedItemFAddr):
        self.renderArea.deleteLater()
        self.mainLayout.removeWidget(self.renderArea)
        self.selectedAddr = selectedItemFAddr
        self.createAreaPercWidget()
    

if __name__ == '__main__':
    # QT parents own their childre
    app = QApplication(sys.argv)
    
    w = Window()
    app.setActiveWindow(w)
    w.show()

    app.exec_()