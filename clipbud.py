#!/usr/bin/env python3

# =============================================================================================
# This program is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# This script must/should come together with a copy of the GNU General Public License. If not,
# access <http://www.gnu.org/licenses/> to find and read it.
#
# Author: Pedro Vernetti G.
# Name: clipbud (Clipboard BackUp Daemon)
#    Keeps a backup (at ~/.clipbu) of the clipboard's content and restores when started
#
# #  In order to have this script working (if it is currently not), install its dependencies:
#    'clipboard' or 'pyperclip'
# =============================================================================================

from sys import argv, stderr
from os import path, environ, access, stat, R_OK, W_OK
from threading import Thread
from time import sleep
try: import clipboard
except: import pyperclip as clipboard



def loop( backupFile, interval ):
    while True:
        sleep(interval)
        content = clipboard.paste()
        if (len(content)):
            with open(backupFile, r'rb') as bu:
                backup = bu.read().decode(r'utf-8', r'ignore')
            if ((len(content) != len(backup)) or (content != backup)):
                with open(backupFile, r'w') as bu:
                    bu.write(content)



if __name__ == r'__main__':
    interval = 60
    try: interval = int(argv[-1])
    except: pass
    backupFile = path.join(environ[r'HOME'], r'.clipbu')
    if (not path.isfile(backupFile)):
        try:
            open(backupFile, r'w')
        except:
            stderr.write("Couldn't create backup file")
            exit(1)
    elif (not (access(backupFile, R_OK) and access(backupFile, W_OK))):
        stderr.write("Couldn't access backup file")
        exit(1)

    if (not clipboard.paste() and stat(backupFile).st_size):
        clipboard.copy(open(backupFile, r'rb').read().decode(r'utf-8', r'ignore'))

    d = Thread(name=r'clipbud', target=loop, args=(backupFile, interval), daemon=True)
    d.start()
