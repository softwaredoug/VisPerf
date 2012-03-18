'''
Created on Mar 10, 2012

Setup.py intended just for using py2exe

@author: Doug
'''
from distutils.core import setup
import py2exe
from version import version

import platform

(wrdSize, os) = platform.architecture()
if wrdSize != "32bit":
    print "Only building 32 bit executables is currently supported"
    exit();


setup(windows=[{'script':'mainWindow.py', 'dest_base':'VisPerf'}],
      options = {
    'py2exe': {
        'dist_dir':("../bin/32/%s" % version),
        'dll_excludes': [
            'MSVCP90.dll'
         ],
        'optimize' : 2
     }
})