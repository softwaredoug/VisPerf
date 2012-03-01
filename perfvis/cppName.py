'''
Created on Feb 29, 2012

@author: Doug
'''


def removeParams(str):
    withoutParams = str.split("(")
    return withoutParams[0]

def removeTemplateArguments(str, depthToRemove):
    """ Remove template arguments deeper than depthToRemove
        so removeTemplateArguments("foo<int>()", 1) gives foo<>()
           removeTemplateArguments("foo< bar<int> >()", 2) gives foo< bar<> >()"""
    if depthToRemove <= 0:
        return str
    currDepth = 0
    res = ""
    for c in str:
        if currDepth < depthToRemove:
            res += c
        if c == "<":
            currDepth += 1
        elif c == ">":
            currDepth -= 1
            if currDepth < depthToRemove:
                res += ">"
    return res
