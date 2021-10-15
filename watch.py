#!/usr/bin/env python

'''
Watch a file for updates and run a callback.
Author: Sachin
Date created: 10/02/2021
'''

from os import stat
from time import sleep

def watch(file, callback, wait=.5):
    '''
    Run a callback every time a file is modified.

    :param file: path to file
    :param callback: function to run on a filename
    :param wait: time in seconds to wait between watches. default=0.5s
    '''
    cache = 0
    
    while True:
        mtime = stat(file).st_mtime
        if cache < mtime:
            cache = mtime
            print(f'Updating {file}...')
            callback(file)

        sleep(wait)

