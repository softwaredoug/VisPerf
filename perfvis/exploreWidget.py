from PySide.QtGui import *
from PySide.QtCore import *
from navhistory import NavHistory


class ExploreControls(QFrame):
    
    __maxFuncSize = 125
    
    newItemSelect = Signal(int)
    
    def __init__(self, parent, funcs):
        QFrame.__init__(self, parent)
        self.isCboxNavigationEnabled = True
        self.history = NavHistory()
        self.layout = QHBoxLayout()
        self.idxToAddr = []
        self.addrToIdx = {}
        
        self.backButton = QPushButton(text="<-", parent=self)
        self.fwdButton = QPushButton(text="->", parent=self)
        
        self.cBox = QComboBox(self)
        self.cBox.setEditable(True)
        self.cBox.setMinimumContentsLength(100)
        self.history.navigateNew(funcs[0][0])
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
        
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setModel(self.cBox.model())
        
        self.cBox.setCompleter(self.completer)
        
        self.cBox.currentIndexChanged.connect(self.cBoxSelected)
        self.backButton.clicked.connect(self.backButtonClicked)
        self.fwdButton.clicked.connect(self.fwdButtonClicked)
        self.layout.addWidget(self.backButton)
        self.layout.addWidget(self.fwdButton)
        self.layout.addWidget(self.cBox)
        self.setLayout(self.layout)
        
    def minimumSizeHint(self):
        return QSize(0,40)

    def updateCbox(self, addr):
        """ Programatically update the combobox 
            (make sure no erroneous navigation events
             occur)"""
        # We intentionally disable navigation because
        # setting the current index programatically looks identical
        # to the user selecting an index, and we don't want
        # the slot to fire infinitely
        self.isCboxNavigationEnabled = False
        self.cBox.setCurrentIndex(self.addrToIdx[addr])
        self.isCboxNavigationEnabled = True
        
    def __navigateTo(self, addr):
        """ Update everything to the specified location """
        self.updateCbox(addr)
        self.newItemSelect.emit(addr) 

    def newNavigation(self, addr):
        """ Represents a new navigation, a branch from
            the current history. As such, everything
            "forward" gets forgotten """
        if addr != self.history.getCurr():
            newAddr = self.history.navigateNew(addr)
            assert newAddr == addr
            self.__navigateTo(newAddr)
            
        
    @Slot(int)
    def cBoxSelected(self, idx):
        """Either the user has selected the combo box
           (in which case we want to navigate a new)
           or some other action has caused this to update
           (in which case we just want to ignore the event"""          
        # We intentionally disable navigation because
        # setting the current index programatically looks identical
        # to the user selecting an index, and we don't want
        # the slot to fire infinitely when its updated
        # from elsewhere
        if not self.isCboxNavigationEnabled:
            return
        self.newNavigation(self.idxToAddr[idx])
        
    @Slot()
    def backButtonClicked(self):
        """ Represents a navigation BACK in
            the current history """
        goBackTo = self.history.goBack()
        self.__navigateTo(goBackTo)

    @Slot()
    def fwdButtonClicked(self):
        """ Represents a navigation FORWARD in
            the current history """
        goFwdTo = self.history.goForward()
        self.__navigateTo(goFwdTo)
        
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
