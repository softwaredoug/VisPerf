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

    
      

class Window(QWidget):
    __initDepth = 2
    
    def createAreaPercWidget(self):
        print "Creating widget for %08x" % self.selectedAddr
        item = CallerCalleePercentageItem(self.report, self.selectedAddr, 100.0)
        #item = TestAreaPercentageItem(100.0)
        geom = QRect(0,0,1024,780)
        self.renderArea = AreaPercentageWidget(geom, item=item, maxAbsDepth = self.selectedDepth)
        self.mainLayout.addWidget(self.renderArea)
        self.renderArea.newItemSelect.connect(self.onNewItemSelectedFromAreaPWidget)
        #self.renderArea.show()
        
    def setupControls(self):
        import cppName
        sortedVals = sorted(self.report.getAllRecords().values(),
                             key = lambda rec: rec.getRoot().getElapsedIncl(),
                             reverse = True)
        self.selectedAddr = sortedVals[0].getRoot().getFunctionAddr()
        self.selectedDepth = Window.__initDepth
        rootFuncs = [(rec.getRoot().getFunctionAddr(),
                      cppName.smartShorten(rec.getRoot().getFunctionName(), 100))
                      for rec in sortedVals]
            
        self.navigateWidget = ExploreControls(parent=self, funcs=rootFuncs, initDepth = Window.__initDepth)
        self.mainLayout.addWidget(self.navigateWidget)
        self.navigateWidget.newItemSelect.connect(self.drawWithNewItem)
        self.navigateWidget.depthChanged.connect(self.drawWithNewDepth)
        self.navigateWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    
    def __init__(self):
        """ Init the window """
        QWidget.__init__(self)
        self.report = loadReport(sys.argv[1])
        self.setWindowTitle("VisPerf - Performance Visualizer -- %s" % sys.argv[1])
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.setupControls()
        self.createAreaPercWidget()
        self.setLayout(self.mainLayout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
    def onNewItemSelectedFromAreaPWidget(self, selectedItemFAddr):
        """ New item selected from the area percent widget,
            we need to use the navigateWidget to provide
            navigation """
        # all navigation goes through the navigateWidget
        self.navigateWidget.newNavigation(selectedItemFAddr)
        
    def redrawAreaPercentWidget(self, selectedItemFAddr, depth):
        """ Delete and redraw the area % widget with the specified
            root function address and depth """
        self.renderArea.deleteLater()
        self.mainLayout.removeWidget(self.renderArea)
        self.selectedAddr = selectedItemFAddr
        self.selectedDepth = depth
        self.createAreaPercWidget()

    
    @Slot(int)
    def drawWithNewItem(self, selectedItemFAddr):
        """ Redraw the underlying area percent widget
            using the specified function addr as the
            root"""
        self.redrawAreaPercentWidget(selectedItemFAddr, self.selectedDepth)
        
    @Slot(int)
    def drawWithNewDepth(self, newMaxDepth):
        print "drawWithNewDepth"
        self.redrawAreaPercentWidget(self.selectedAddr, newMaxDepth)
        
    

if __name__ == '__main__':
    # QT parents own their childre
    app = QApplication(sys.argv)
    
    w = Window()
    app.setActiveWindow(w)
    w.show()

    app.exec_()
