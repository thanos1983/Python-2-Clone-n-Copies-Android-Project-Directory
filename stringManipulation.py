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

        """
        :rtype: self.replace_string (True, False)
        """
        self.output = output
        self.strings_file = strings_file
        self.regex_string = regex_string
        self.build_gradle = build_gradle
        self.replace_string = replace_string
        self.bash_cmd_return = bash_cmd_return
        self.android_manifest_file = android_manifest_file

    def get_android_manifest_xml(self, app_section):
        """
        :rtype: Return the path of the AndroiManifest.xml file
        :type app_section: Each directory has a different section name to use for each clone
        """
        working_directory = os.getcwd()
        # Create path for 'AndroidManifest.xml' file based on directory
        manifest_xml = working_directory + "/" + app_section + "/app/src/main/AndroidManifest.xml"
        self.android_manifest_file = manifest_xml
        return self.android_manifest_file

    def execute_bash_cmd(self, cmd):
        """
        :type cmd: Command to execute on terminal
        """
        result = subprocess.check_output(cmd, shell=True)
        self.bash_cmd_return = result
        return self.bash_cmd_return

    def get_strings_xml(self, app_section):
        """
        :type app_section: Each directory has a different section name to use for each clone
        """
        working_directory = os.getcwd()
        # Search for 'strings.xml' file
        find_strings = "find " + working_directory + "/" + app_section + "/ -name 'strings.xml'"
        strings_xml_path = self.execute_bash_cmd(find_strings)
        # Strip new line character
        strings_xml_path = strings_xml_path.rstrip('\r\n')
        self.strings_file = strings_xml_path
        return self.strings_file

    def get_build_gradle_app(self, app_section):
        """
        :param app_section: Each directory has a different section name to use for each clone
        :rtype: Path to the specified builde.gradle file based on section of configuration.ini file
        """
        working_directory = os.getcwd()
        # Create path for 'build.gradle' file based on directory
        build_gradle = working_directory + "/" + app_section + "/app/build.gradle"
        self.build_gradle = build_gradle
        return self.build_gradle

    def str_regex(self, file_input, regex_key):
        # Open file and get matching string based on regex
        """
        :param regex_key: Find all occurrences based on regex input
        :param file_input: File input to use regex
        :rtype: self.regex_string returns string matched based on regex
        """
        with open(file_input, "r") as fr:
            str_data = fr.read()
            str_line = re.findall(r'{}'.format(regex_key), str_data)
        fr.closed
        self.regex_string = str_line[0]
        return self.regex_string

    def str_replace(self, file_input, str_old, str_new):
        # Replace all occurrences of string where is matched
        """
        :rtype: self.replace_string returs True or False if the process found strings to replace
        :param str_new: Replace all occurrences found from str_old string
        :param str_old: Find all occurrences based on input string
        :type file_input: File input to use to replace string
        """
        for line in fileinput.input(file_input, inplace=True):
            if line:
                line = re.sub(str_old, str_new, line.rstrip())
                print(line)
                self.replace_string = True
            else:
                self.replace_string = False
        fileinput.close()
        return self.replace_string
