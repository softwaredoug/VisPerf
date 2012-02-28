'''
Created on Feb 25, 2012

@author: Doug
'''

class LabeledCsvEntry(object):
    def __init__(self, header, entry):
        if not type(header) is list:
            raise ValueError("Header is not list")
        if not type(entry) is list:
            raise ValueError("Entry is not list")
        if len(header) != len(entry):
            raise ValueError("Impossible for header to represent entry, header len != entryLen: %i != %i"
                             % (len(header), len(entry)))
        else:
            self.fields = dict(zip(header, entry))
            
    def getHeader(self):
        return self.fields.keys()
    
    def getValues(self):
        return self.fields.values()