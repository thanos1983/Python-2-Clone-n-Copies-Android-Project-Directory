#!/usr/bin/python

import os
import re
import fileinput
import subprocess


class StringManipulationProcess(object):
    """This class is for manipulating string(s) necessary for our purposes."""

    def __init__(self,
                 output=None,
                 strings_file=None,
                 regex_string=None,
                 build_gradle=None,
                 replace_string=None,
                 bash_cmd_return=None,
                 android_manifest_file=None):

        self.output = output
        self.strings_file = strings_file
        self.regex_string = regex_string
        self.build_gradle = build_gradle
        self.replace_string = replace_string
        self.bash_cmd_return = bash_cmd_return
        self.android_manifest_file = android_manifest_file

    def get_android_manifest_xml(self, app_section):
        working_directory = os.getcwd()

        # Create path for 'AndroidManifest.xml' file based on directory
        manifest_xml = working_directory + "/" + app_section + "/app/src/main/AndroidManifest.xml"

        self.android_manifest_file = manifest_xml
        return self.android_manifest_file

    def execute_bash_cmd(self, cmd):
        result = subprocess.check_output(cmd, shell=True)
        self.bash_cmd_return = result
        return self.bash_cmd_return

    def get_strings_xml(self, app_section):
        working_directory = os.getcwd()

        # Search for 'strings.xml' file
        find_strings = "find " + working_directory + "/" + app_section + "/ -name 'strings.xml'"
        strings_xml_path = self.execute_bash_cmd(find_strings)

        # Strip new line character
        strings_xml_path = strings_xml_path.rstrip('\r\n')

        self.strings_file = strings_xml_path
        return self.strings_file

    def get_build_gradle_app(self, app_section):
        working_directory = os.getcwd()

        # Create path for 'AndroidManifest.xml' file based on directory
        build_gradle = working_directory + "/" + app_section + "/app/build.gradle"

        self.android_manifest_file = build_gradle
        return self.android_manifest_file

    def str_regex(self, file_input, str_old, str_new):
        # Open file and get matching string based on regex
        with open(file_input, "r") as fr:
            str_data = fr.read()
            str_line = re.findall(r'{}'.format(str_old), str_data)
        fr.closed
        print "XML: {}".format(str_line)

        self.regex_string = str_line[0]
        return self.regex_string

    def str_replace(self, file_input, str_old, str_new):
        # Replace all occurrences of string where is matched
        for line in fileinput.input(file_input, inplace=True):
            line = re.sub(str_old, str_new, line.rstrip())
            print(line)
        fileinput.close()
        print "File Input: {}\nStr Old: {}\Str New: {}" .format(file_input, str_old, str_new)

        self.replace_string = line
        return self.replace_string
