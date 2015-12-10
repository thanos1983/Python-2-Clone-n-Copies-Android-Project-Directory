#!/usr/bin/python

import re
import os
import fileinput
import subprocess
import pprint


class RenamingProcess(object):
    """This class is for modifying the package name in the AndroidManifest.xml file
        and also the application name. e.g. application android:icon="@drawable/icon" android:label="new name"
        Secondly modifying all renaming all instances of main package."""

    def __init__(self, output=None, manifests_file=None, modified_file=None):
        """

        :rtype: object.output String with success or Error
        """
        self.output = output
        self.modified_file = modified_file
        self.manifests_file = manifests_file

    def find_name(self, cmd):
        result = subprocess.check_output(cmd, shell=True)
        self.manifests_file = result
        return result

    def str_replace(self, file_input, str_old,  str_new):
        print "File Input {}" .format(file_input)
        for line in fileinput.input(file_input, inplace=True):
            print "Line: {}" .format(line)
            print line.replace(str_old, str_new)

    def modification_process(self, app_section_name, data_conf_file):
        working_directory = os.getcwd()

        # Search for 'manifests' file
        find_manifests = "find " + working_directory + "/" + app_section_name + "/ -iname manifests"
        manifests_path = self.find_name(find_manifests)

        # Search for 'AndroidManifest.xml' file
        str_manifests_path = str(manifests_path)
        # Strip new line character
        str_manifests_path = str_manifests_path.rstrip('\r\n')
        find_manifest_xml = "find " + str_manifests_path + "/ -iname 'AndroidManifest.xml'"
        manifest_xml = self.find_name(find_manifest_xml)

        # Strip new line character
        manifest_xml = manifest_xml.rstrip('\r\n')

        # Retrieve package PackageName from '*.ini' file
        key, package_name = data_conf_file[app_section_name][0]

        # Replace package name in 'AndroidManifest.xml' file
        #self.str_replace(manifest_xml, key, package_name)



        # print manifest_xml
        # return self.output
