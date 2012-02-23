
from PySide.QtCore import *
import copy

def validRectInAndReturned(fn):
    """ Decorator to validate the input/output rectangles
       are indeed valid """
    def callWithValidRects(rect, *args, **kwargs):
        if not rect.isValid():
            raise ValueError("Invalid rectangle given as argument: %s" % str(rect))
        rVal = fn(rect, *args, **kwargs)
        if not rVal.isValid():
            raise ValueError("Operation produced an invalid rectangle: %s, rect: %s, args: %s, kwargs %s" % 
                                (str(rVal), str(rect), str(args), str(kwargs)))
        return rVal
    return callWithValidRects

def validRectReturned(fn):
    """ Decorator to validate the input/output rectangles
       are indeed valid """
    def callWithValidRects(*args, **kwargs):
        rVal = fn(*args, **kwargs)
        if not rVal.isValid():
            raise ValueError("Operation produced an invalid rectangle: %s, args: %s, kwargs %s" % 
                                (str(rVal), str(args), str(kwargs)))
        return rVal
    return callWithValidRects
    


@validRectInAndReturned
def normalize(rect):
    """ Translate a rectangle to x,y of 0,0 """
    rVal = QRect()
    (height, width) = (rect.height(), rect.width())
    rVal.setX(0)
    rVal.setY(0)
    rVal.setHeight(height)
    rVal.setWidth(width)
    return rVal

@validRectInAndReturned
def scaleLockCenter(rect, resizeMult):
    """ Shrink a rect based on the resizeMult, ie
        if 1.2 passed in, its 1.2 times larger with
        the same center"""
    shrunkRect = copy.deepcopy(rect)
    shrunkRect.setWidth(rect.width() * resizeMult )
    shrunkRect.setHeight(rect.height() * resizeMult )
    dx = rect.center().x() - shrunkRect.center().x() 
    dy = rect.center().y() - shrunkRect.center().y()
    shrunkRect.translate(dx, dy)
    return shrunkRect

@validRectInAndReturned
def moveCornersTowardCenter(rect, deltaX, deltaY):
    """ Bring in the corners by deltaX and deltaY
        but keep the center the same
        """
    shrunkRect = QRect()
    ur = QPoint()
    lL = QPoint()
    tL = rect.topLeft()
    bR = rect.bottomRight()
    tL.setX(tL.x() + deltaX)
    tL.setY(tL.y() + deltaY)
    bR.setX(bR.x() - deltaX)
    bR.setY(bR.y() - deltaY)
    if isinstance(rect,QRectF):
        tL = tL.toPoint()
        bR = bR.toPoint()
    shrunkRect.setTopLeft(tL)
    shrunkRect.setBottomRight(bR)
    return shrunkRect