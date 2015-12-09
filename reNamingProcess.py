#!/usr/bin/python

import os
import subprocess


class RenamingProcess(object):
    """This class is for modifying the package name in the AndroidManifest.xml file
        and also the application name. e.g. application android:icon="@drawable/icon" android:label="new name"
        Secondly modifying all renaming all instances of main package."""

# 1) pwd
# 2) find ~/Desktop/gcmTestEnvironment/ -iname "manifests"
# 3) find /Users/thanos/Desktop/gcmTestEnvironment//app/build/intermediates/manifests -name "AndroidManifest.xml"

    def __init__(self, output=None):
        """

        :rtype: object.output String with success or Error
        """

        self.output = output

    def modification_process(self, source_file, target_file):
        working_directory = os.getcwd()

        print working_directory


""""command = "ls -la"  # the shell command
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# Launch the shell command:
output, error = process.communicate()

if output:
    print "Output: " .format(output)
elif error:
    print "Error: " .format(error)"""

