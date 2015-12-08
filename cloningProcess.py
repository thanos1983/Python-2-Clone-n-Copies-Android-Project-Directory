#!/usr/bin/python

import errno
import shutil
from shutil import copy, copytree, ignore_patterns


class DuplicationProcess(object):
    """Class cloning (copying) Directories or files and also ignore file(s) to avoid processing.
    Caution: directories or file(s) will not be processed (copied) if they do exist already."""

    def __init__(self, output=None):
        """

        :rtype: object.output String
        """

        self.output = output

    def clone(self, source_file, target_file):
        """

        :param self: Instance attribute(s)
        :param source_file: Source file to clone
        :param target_file: Target file name
        :rtype: object containing the success or error
        """
        try:
            shutil.copytree(source_file, target_file, ignore=ignore_patterns('*.*~'))  # More files add: , '*.sh',
            self.output = 'Success'
            return self.output
        except OSError as e:  # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(source_file, target_file)
                self.output = 'Success'
                return self.output
            else:
                self.output = 'Error: {}'.format(e)
                return self.output
