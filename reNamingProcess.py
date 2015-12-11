#!/usr/bin/python

import os
import re
import subprocess
import pprint


class RenamingProcess(object):
    """This class is for modifying the package name in the AndroidManifest.xml file
        and also the application name. e.g. application android:icon="@drawable/icon" android:label="new name"
        Secondly modifying all renaming all instances of main package."""

    def __init__(self,
                 output=None,
                 modified_file=None,
                 manifests_file=None,
                 replace_string=None,
                 android_manifests_file=None):
        """

        :rtype: object.output String with success or Error
        """
        self.output = output
        self.modified_file = modified_file
        self.manifests_file = manifests_file
        self.replace_string = replace_string
        self.android_manifests_file = android_manifests_file

    def find_name(self, cmd):
        result = subprocess.check_output(cmd, shell=True)
        self.manifests_file = result
        return result

    def get_android_manifest_xml(self, app_section_name):
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

        self.android_manifests_file = manifest_xml
        return self.android_manifests_file

    def str_replace(self, file_input, str_old, str_new):
        with open(file_input, 'r') as my_file:
            xml_data = my_file.read()
            xml_data = re.sub(r'{}=\"(.+?)\"'.format(str_old), str_new, xml_data)
        my_file.closed
        self.replace_string = xml_data
        return self.replace_string

    def modification_process(self, app_section_name, data_conf_file):
        android_manifest_xml = self.get_android_manifest_xml(app_section_name)

        # Retrieve package PackageName from '*.ini' file
        key, package_new_name = data_conf_file[app_section_name][0]

        # Replace package name in 'AndroidManifest.xml' file
        replace_str_return = self.str_replace(android_manifest_xml, key, package_new_name)

        print "String replace return: {}" .format(replace_str_return)
        exit(1)

        # print manifest_xml
        # return self.output
