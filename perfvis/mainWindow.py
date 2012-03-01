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
        print "Creating widget for %08x" % self.selectedAddr
        item = CallerCalleePercentageItem(self.report, self.selectedAddr, 100.0)
        #item = TestAreaPercentageItem(100.0)
        geom = QRect(0,0,1024,780)
        self.renderArea = AreaPercentageWidget(geom, item=item)

        self.mainLayout.addWidget(self.renderArea)
              
        self.renderArea.newItemSelect.connect(self.onNewItemSelectedFromAreaPWidget)
        #self.renderArea.show()
        
    def setupControls(self):
        import cppName
        sortedVals = sorted(self.report.getAllRecords().values(),
                             key = lambda rec: rec.getRoot().getElapsedIncl(),
                             reverse = True)
        self.selectedAddr = sortedVals[0].getRoot().getFunctionAddr()
        rootFuncs = [(rec.getRoot().getFunctionAddr(), cppName.removeTemplateArguments(cppName.removeParams(rec.getRoot().getFunctionName()), 2))
                      for rec in sortedVals]
            
        self.navigateWidget = ExploreControls(parent=self, funcs=rootFuncs)
        self.mainLayout.addWidget(self.navigateWidget)
        self.navigateWidget.newItemSelect.connect(self.drawWithNewItem)
        #self.navigateWidget.show()

    
    def __init__(self):
        QWidget.__init__(self)
        self.report = loadReport(sys.argv[1])
        self.setWindowTitle(tr("Basic Drawing"))
        self.mainLayout = QVBoxLayout()
        self.setupControls()
        self.createAreaPercWidget()
        
        self.setLayout(self.mainLayout)
        
    def onNewItemSelectedFromAreaPWidget(self, selectedItemFAddr):
        # all navigation goes through the navigateWidget
        self.navigateWidget.navigateTo(selectedItemFAddr)

    
    @Slot(int)
    def drawWithNewItem(self, selectedItemFAddr):
        """ Redraw with the specified item """
        print "Draw with new item %08x" % selectedItemFAddr
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