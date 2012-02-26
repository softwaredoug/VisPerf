from PySide.QtGui import *
from PySide.QtCore import *

class ExploreControls(QWidget):
    
    __maxFuncSize = 125
    
    newItemSelect = Signal(int)
    
    def __init__(self, parent, funcs):
        QWidget.__init__(self, parent)
        self.idxToAddr = []
        self.cBox = QComboBox(self)
        for (funcAddr, funcName) in funcs:
            if len(funcName) < self.__maxFuncSize:
                label = "%s" % funcName
            else:
                label = "%s" % funcName[-self.__maxFuncSize:]
            self.cBox.addItem(label)
            self.idxToAddr.append(funcAddr)
        self.cBox.currentIndexChanged.connect(self.cBoxSelected)
        
    def minimumSizeHint(self):
        return QSize(0, 50)
        #return self.cBox.minimumSizeHint()
    
    @Slot(int)
    def cBoxSelected(self, idx):
        self.newItemSelect.emit(self.idxToAddr[idx])
        
        

        
    