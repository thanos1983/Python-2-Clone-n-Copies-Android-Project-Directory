#!/usr/bin/python

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

    @staticmethod
    def in_place(file_input, str_old, str_new):
        for line in fileinput.input(file_input, inplace=True):
            print line.replace(str_old, str_new)

    """def in_place_editing(input_file, text_to_search, text_to_replace):
        with open(, "wt") as fout:
            with open("Stud.txt", "rt") as fin:
                for line in fin:
                    print "I found line: {}" .format()
                    #fout.write(line.replace(text_to_search, text_to_replace))"""

    def modification_process(self, source_file, app_section_name, data_conf_file):
        working_directory = os.getcwd()

        # Search for 'manifests' file
        find_manifests = "find " + working_directory + "/" + source_file + "/ -iname manifests"
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
        in_place(manifest_xml, key, package_name)



        # print manifest_xml
        # return self.output
