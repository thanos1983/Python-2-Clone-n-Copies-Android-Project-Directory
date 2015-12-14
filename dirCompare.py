#!/usr/bin/python

import sys
import filecmp
import StringIO


class DirectoryComparisonProcess(object):
    """This class is used to compare and find difference two directories (dirA, dirB)."""

    def __init__(self, output=None):
        self.output = output

    def retrieve_dir_diff(self, dir1, dir2):
        # Capture stdout from directory diff
        old_stdout = sys.stdout
        capturer = StringIO.StringIO()
        sys.stdout = capturer

        # Call functions/ methods
        dc = filecmp.dircmp(dir1, dir2).report_full_closure()
        sys.stdout = old_stdout

        # Split captured output into a list
        output = capturer.getvalue().splitlines()

        if output[7]:
            diff_dir1 = output[7].split()
            diff_dir2 = output[8].split()

            print '{}\n{}' .format(diff_dir1, diff_dir2)
        else:
            print 'No difference between dir: {} and dir: {}' .format(dir1, dir2)

        exit(1)
        self.output = output
        return self.output
