'''
Created on Mar 10, 2012

@author: Doug
'''
from distutils.core import setup
import py2exe



setup(windows=['mainWindow.py'],
      options = {
    'py2exe': {
        'dist_dir':"../bin/64/",
        'dll_excludes': [
            'MSVCP90.dll'
         ]
     }
})