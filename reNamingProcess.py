#!/usr/bin/python

import os
import fileinput
import subprocess


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

    def in_place_editing(self, input_file, text_to_search, text_to_replace):
        with open(input_file, "wt") as fout:
            with open("Stud.txt", "rt") as fin:
                for line in fin:
                    fout.write(line.replace(text_to_search, text_to_replace))

    def modification_process(self, source_file):
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
        # ToDo When I need to process the data from the conf file here is the code
        # for name, value in parser_obj.items(section_name):
        # print '  %s = %s' % (name, value)

        # Replace package name in 'AndroidManifest.xml' file

        print manifest_xml
        # return self.output
