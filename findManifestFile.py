#!/usr/bin/python

import os
import subprocess

# 1) pwd
# 2) find ~/Desktop/gcmTestEnvironment/ -iname "manifests"
# 3) find /Users/thanos/Desktop/gcmTestEnvironment//app/build/intermediates/manifests -name "AndroidManifest.xml"

working_directory = os.getcwd()

print os.listdir()


""""command = "ls -la"  # the shell command
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# Launch the shell command:
output, error = process.communicate()

if output:
    print "Output: " .format(output)
elif error:
    print "Error: " .format(error)"""

