#!/usr/bin/python

import errno
import shutil
from shutil import copy, copytree, ignore_patterns


class DuplicationProcess(object):
    """Class cloning (copying) Directories and also ignore file(s) to avoid processing.
       Caution: directories will not be processed (copied) if they do exist already."""

    def __init__(self, output=None):
        """

        :rtype: object.output String with success or Error
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
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: {}' .format(e))
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: {}' .format(e))
