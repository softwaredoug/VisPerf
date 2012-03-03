'''
Created on Feb 29, 2012

@author: Doug
'''


def removeParams(cppFuncName):
    """ Remove everything after the () of a function name
        >>> removeParams("foo()")
        'foo'
        >>> removeParams("foo()()")
        'foo'
        """
    withoutParams = cppFuncName.split("(")
    return withoutParams[0]

def removeTemplateArguments(cppFuncName, depthToRemove):
    """ Remove template arguments deeper than depthToRemove,
        including the angle brackets

        >>> removeTemplateArguments("foo<int>()", 1)
        'foo()'
        >>> removeTemplateArguments("foo< bar<int> >()", 2)
        'foo< bar >()'
        >>> removeTemplateArguments("foo< bar >()", 2)
        'foo< bar >()'
        >>> removeTemplateArguments("foo< bar >()", 0)
        ''
        """
    currDepth = 0
    res = ""
    for c in cppFuncName:
        if c == "<":
            currDepth += 1
        if currDepth < depthToRemove:
            res += c
            added = True
        elif c == ">":
            currDepth -= 1
    return res

def smartShorten(cppFuncName, desiredLen):
    """ Shorten the function name to the desired length by
        1. always remove the parameters
        2. keep removing template arguments until the length is satisfied
        3. as a last resort, trim from the front

        >>> smartShorten("foo<int>()", 1000)
        'foo<int>'
        >>> smartShorten("foo<int>()", 9)
        'foo<int>'
        >>> smartShorten("foo<int>()", 3)
        'foo'
        >>> smartShorten("foo<int>()", 2)
        'oo'
    """
    cppFuncName = removeParams(cppFuncName)
    currDepth = 5
    while len(cppFuncName) > desiredLen and currDepth > 0:
        cppFuncName = removeTemplateArguments(cppFuncName, currDepth)
        currDepth -= 1
    return cppFuncName[-desiredLen:]
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()
