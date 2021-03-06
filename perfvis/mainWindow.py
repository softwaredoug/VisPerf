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

    
      

class MainWindow(QWidget):
    __initDepth = 2
    
    def createAreaPercWidget(self):
        item = CallerCalleePercentageItem(self.report, self.selectedAddr, 100.0)
        #item = TestAreaPercentageItem(100.0)
        geom = QRect(0,0,1024,780)
        self.renderArea = AreaPercentageWidget(geom, rootFunction=item, maxAbsDepth = self.selectedDepth)
        #self.renderArea.setGeometry(geom)
        self.mainLayout.addWidget(self.renderArea)
        self.renderArea.newRootFunctionSelected.connect(self.onNewItemSelectedFromAreaPWidget)
        #self.renderArea.show()
        
    def setupControls(self):
        import cppName
        sortedVals = sorted(self.report.getAllRecords().values(),
                             key = lambda rec: rec.getRoot().getElapsedIncl(),
                             reverse = True)
        self.selectedAddr = sortedVals[0].getRoot().getFunctionAddr()
        self.selectedDepth = MainWindow.__initDepth
        rootFuncs = [(rec.getRoot().getFunctionAddr(),
                      cppName.smartShorten(rec.getRoot().getFunctionName(), 100))
                      for rec in sortedVals]
            
        self.navigateWidget = ExploreControls(parent=self, funcs=rootFuncs, initDepth = MainWindow.__initDepth)
        self.mainLayout.addWidget(self.navigateWidget)
        self.navigateWidget.newRootFunctionSelected.connect(self.drawWithNewItem)
        self.navigateWidget.depthChanged.connect(self.drawWithNewDepth)
        self.navigateWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    
    def __init__(self, callerCalleeCsvFname):
        """ Init the window """
        from version import version
        QWidget.__init__(self)
        self.report = loadReport(callerCalleeCsvFname)
        self.setWindowTitle("VisPerf v%s -- %s" % (version, callerCalleeCsvFname))
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
        self.redrawAreaPercentWidget(self.selectedAddr, newMaxDepth)
        
    

if __name__ == '__main__':
    # QT parents own their childre
    app = QApplication(sys.argv)
    
    if len(sys.argv) != 2:
        callerCalleeCsvFname = QFileDialog.getOpenFileName(None, "Open Caller-Callee csv", "C:/", "Csv Files (*.csv)")
        callerCalleeCsvFname = callerCalleeCsvFname[0]
    else:
        callerCalleeCsvFname = sys.argv[1]
    print callerCalleeCsvFname
        
    w = MainWindow(callerCalleeCsvFname)
    app.setActiveWindow(w)
    w.show()

    app.exec_()
