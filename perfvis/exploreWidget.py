from PySide.QtGui import *
from PySide.QtCore import *

class ExploreControls(QWidget):
    
    __maxFuncSize = 125
    
    newItemSelect = Signal(int)
    
    def __init__(self, parent, funcs):
        QWidget.__init__(self, parent)
        self.cBoxUserSelected = True
        self.history = []
        self.layout = QHBoxLayout()
        self.idxToAddr = []
        self.addrToIdx = {}
        self.backButton = QPushButton(text="<-", parent=self)
        self.cBox = QComboBox(self)
        self.history = [funcs[0][0]]
        currIdx = 0
        for (funcAddr, funcName) in funcs:
            if len(funcName) < self.__maxFuncSize:
                label = "%s" % funcName
            else:
                label = "%s" % funcName[-self.__maxFuncSize:]
            self.cBox.addItem(label)
            self.idxToAddr.append(funcAddr)
            self.addrToIdx[funcAddr] = currIdx
            currIdx += 1
        self.cBox.currentIndexChanged.connect(self.cBoxSelected)
        self.backButton.clicked.connect(self.backButtonClicked)
        self.layout.addWidget(self.backButton)
        self.layout.addWidget(self.cBox)
        self.setLayout(self.layout)
        
    def minimumSizeHint(self):
        return QSize(0,40)
        
    def navigateTo(self, addr):
        self.cBoxUserSelected = False
        self.cBox.setCurrentIndex(self.addrToIdx[addr])
        self.cBoxUserSelected = True
        self.newItemSelect.emit(addr)
        self.history.append(addr)
        
        
    def goBack(self):      
        if len(self.history) >= 2:
            self.history.pop(-1)
            goBackTo = self.history[-1]
            print "Going back to %08x" % goBackTo
            self.cBox.setCurrentIndex(self.addrToIdx[goBackTo])
            self.newItemSelect.emit(goBackTo)
        
    @Slot(int)
    def cBoxSelected(self, idx):
        if self.cBoxUserSelected:
            self.navigateTo(self.idxToAddr[idx])
        
    @Slot()
    def backButtonClicked(self):
        print "Back Button bitches!!"
        self.goBack()
        
        

        
    