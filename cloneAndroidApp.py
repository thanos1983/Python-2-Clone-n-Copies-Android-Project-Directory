#!/usr/bin/python

import sys
import errno
import shutil
from shutil import copy, copytree, ignore_patterns

"""The script can copy Directories or files and also ignore file(s) to avoid processing.
    Caution: directories or file(s) will not be processed (copied) if they do exist."""


def copy(source_file, target_file):
    try:
        shutil.copytree(source_file, target_file, ignore=ignore_patterns('*.*~'))  # More files add: , '*.sh',
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(source_file, target_file)
        else:
            print('Directory not copied. Error: %s' % e)

if len(sys.argv) != 4:
    print "Usage: python {} [Android App Dir. SRC] [Number of Copies] [Android App Dir. DST]".format(sys.argv[0])
    sys.exit(1)
elif not sys.argv[2].isdigit():
    print "Please enter a valid number of copies"
    sys.exit(1)

sys.argv[3] = sys.argv[3].translate(None, '/')

for i in range(int(sys.argv[2])):
    copy(sys.argv[1], sys.argv[3] + '{}'.format(i))
