from PySide.QtGui import *
from PySide.QtCore import *

class NavHistory(object):
    """ Represents a navigation history similar to that of a browser
        you can go back and forward all you want until you navigate
        to a brand new place, then everything "forward" from where
        you are now goes away

        >>> n = NavHistory()
        >>> n.navigateNew(1)
        1
        >>> n.navigateNew(2)
        2
        >>> n.navigateNew(3)
        3
        >>> n.goBack()
        2
        >>> n.goBack()
        1
        >>> n.goBack()
        1
        >>> n.goForward()
        2
        >>> n.goForward()
        3
        >>> n.goForward()
        3
        >>> n.goBack()
        2
        >>> n.navigateNew(4)
        4
        >>> n.goForward()
        4
        >>> n.goBack()
        2
        >>> n.goBack()
        1
        """
    def __init__(self):
        self.history = []
        self.currLoc = -1

    def goBack(self):
        if self.currLoc > 0:
            self.currLoc -= 1
        return self.history[self.currLoc]

    def goForward(self):
        if self.currLoc + 1 < len(self.history):
            self.currLoc += 1
        return self.history[self.currLoc]

    def navigateNew(self, location):
        self.history = self.history[:self.currLoc+1]
        self.currLoc += 1
        self.history.append(location)
        return self.history[self.currLoc]

    def getCurr(self):
        if self.currLoc < 0 or self.currLoc > len(self.history):
            raise ValueError("History is empty or invalid")
        return self.history[self.currLoc]

    def __repr__(self):
        return repr(self.history)
    

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
        # We intentionally disable navigation because
        # setting the current index programatically looks identical
        # to the user selecting an index, and we don't want
        # the slot to fire infinitely
        self.isCboxNavigationEnabled = False
        self.cBox.setCurrentIndex(self.addrToIdx[addr])
        self.isCboxNavigationEnabled = True
        
    def __navigateTo(self, addr):
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
