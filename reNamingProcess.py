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
                 strings_file=None,
                 modified_file=None,
                 manifests_dir=None,
                 replace_string=None,
                 android_manifests_file=None):
        """

        :rtype: object.output String with success or Error
        """
        self.output = output
        self.strings_file = strings_file
        self.modified_file = modified_file
        self.manifests_dir = manifests_dir
        self.replace_string = replace_string
        self.android_manifests_file = android_manifests_file

    def execute_bash_cmd(self, cmd):
        result = subprocess.check_output(cmd, shell=True)
        self.manifests_dir = result
        return self.manifests_dir

    def get_strings_xml(self, app_section):
        working_directory = os.getcwd()

        # Search for 'strings.xml' file
        find_strings = "find " + working_directory + "/" + app_section + "/ -name 'strings.xml'"
        strings_xml_path = self.execute_bash_cmd(find_strings)

        # Strip new line character
        strings_xml_path = strings_xml_path.rstrip('\r\n')

        self.strings_file = strings_xml_path
        return self.strings_file

    def get_android_manifest_xml(self, app_section):
        working_directory = os.getcwd()

        # Search for 'manifests' dir
        find_manifests = "find " + working_directory + "/" + app_section + "/ -name 'manifests'"
        manifests_path = self.execute_bash_cmd(find_manifests)

        # Search for 'AndroidManifest.xml' file
        str_manifests_path = str(manifests_path)

        # Strip new line character
        str_manifests_path = str_manifests_path.rstrip('\r\n')
        find_manifest_xml = "find " + str_manifests_path + "/ -name 'AndroidManifest.xml'"
        manifest_xml = self.execute_bash_cmd(find_manifest_xml)

        # Strip new line character
        manifest_xml = manifest_xml.rstrip('\r\n')

        self.android_manifests_file = manifest_xml
        return self.android_manifests_file

    def str_replace(self, file_input, str_old, str_new):
        with open(file_input, "r") as fr:
            xml_data = fr.read()
            xml_data = re.sub(r"{}".format(str_old), str_new, xml_data)
        fr.closed

        with open(file_input, "w") as fw:
            fw.write(xml_data)
        fw.closed

        self.replace_string = xml_data
        return self.replace_string

    def modification_process(self, app_section_name, data_conf_file):
        android_manifest_xml = self.get_android_manifest_xml(app_section_name)

        # Retrieve package PackageName from '*.ini' file
        key, new_package = data_conf_file[app_section_name][0]

        # Adding equal sign
        key = + '=' + '\"(.+?)\"'

        # Replace package name in 'AndroidManifest.xml' file
        self.str_replace(android_manifest_xml, key, new_package)

        # Retrieve package PackageName from '*.ini' file
        key, new_icon = data_conf_file[app_section_name][1]

        # Adding Android prefix
        key = 'android:' + key + '=' + '\"(.+?)\"'

        # Replace Android icon name in 'AndroidManifest.xml' file
        self.str_replace(android_manifest_xml, key, new_icon)

        # Replace Android Label name in 'strings.xml' file
        strings_xml = self.get_strings_xml(app_section_name)

        # Retrieve label android:label from '*.ini' file
        key, new_label = data_conf_file[app_section_name][2]

        key = '<string name=\"app_name\">.*</string>'
        # self.str_replace(android_manifest_xml, key, new_icon)
        # print self.str_replace(strings_xml, key, new_label)
        print self.str_replace(strings_xml, key, new_label)
        exit(1)

        # print manifest_xml
        # return self.output
