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
        """ Go back, return the new curren location """
        if self.currLoc > 0:
            self.currLoc -= 1
        return self.history[self.currLoc]

    def goForward(self):
        """ Go forward, return the new curren location """
        if self.currLoc + 1 < len(self.history):
            self.currLoc += 1
        return self.history[self.currLoc]

    def navigateNew(self, location):
        """ Navigate in a new direction, meaning everything
           thats forward is no longer valid and will be deleted.
           Similar to fwd/back, returns current location
           """
        self.history = self.history[:self.currLoc+1]
        self.currLoc += 1
        self.history.append(location)
        return self.history[self.currLoc]

    def getCurr(self):
        """ Get the current location """
        if self.currLoc < 0 or self.currLoc > len(self.history):
            raise ValueError("History is empty or invalid")
        return self.history[self.currLoc]

    def __repr__(self):
        return repr(self.history)

if __name__ == "__main__":
    import doctest
    doctest.testmod()