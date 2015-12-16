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
                 list_package_name=None,
                 gradlew_std_output=None,
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
        self.list_package_name = list_package_name
        self.gradlew_std_output = gradlew_std_output
        self.android_manifest_file = android_manifest_file

    def compile_and_build_project(self, app_section):

        working_directory = os.getcwd()
        path = working_directory + "/" + app_section
        os.chdir(path)

        gradlew_build = './gradlew build'
        self.gradlew_std_output = self.execute_bash_cmd(gradlew_build)
        print "Build: {}" .format(self.gradlew_std_output)
        exit(1)
        return self.gradlew_std_output

    def get_list_of_package_name_files(self, app_section):
        """
        list all occurrences of 'package=what.ever.here'. We do not care about debug 'package=etc' because it will
        reproduce the files for us automatically when we will compile the app by running ./gradlew build

        :param app_section: Each directory has a different section name to use for each clone
        """

        working_directory = os.getcwd()
        dir_package_name = working_directory + "/" + app_section + "/app/src/"
        cmd = 'grep -rl "package=*" ' + dir_package_name
        self.list_package_name = self.execute_bash_cmd(cmd)
        self.list_package_name = self.list_package_name.split('\n')
        self.list_package_name = filter(None, self.list_package_name)
        return self.list_package_name

    def get_android_manifest_xml(self, app_section):
        """
        Get path for strings.xml file

        :rtype: Return the path of the AndroiManifest.xml file
        :type app_section: Each directory has a different section name to use for each clone
        """

        working_directory = os.getcwd()
        self.android_manifest_file = working_directory + "/" + app_section + "/app/src/main/AndroidManifest.xml"
        return self.android_manifest_file

    def execute_bash_cmd(self, cmd):
        """
        Execute any command in terminal and capture the std.output

        :rtype: Return the std.output of the cmd
        :type cmd: Command to execute on terminal
        """

        try:
            self.bash_cmd_return = subprocess.check_output(cmd, shell=True)
        except CalledProcessError as e:
            self.bash_cmd_return = e.self.bash_cmd_return
        return self.bash_cmd_return

    def get_strings_xml(self, app_section):
        """
        Get path for strings.xml file

        :rtype: Path to the specified strings.xml file based on section of configuration.ini file
        :type app_section: Each directory has a different section name to use for each clone
        """

        working_directory = os.getcwd()
        self.strings_file = working_directory + "/" + app_section + "/app/src/main/res/values/strings.xml"
        return self.strings_file

    def get_build_gradle_app(self, app_section):
        """
        Get path for build.gradle file

        :param app_section: Each directory has a different section name to use for each clone
        :rtype: Path to the specified builde.gradle file based on section of configuration.ini file
        """

        working_directory = os.getcwd()
        self.build_gradle = working_directory + "/" + app_section + "/app/build.gradle"
        return self.build_gradle

    def str_regex(self, file_input, regex_key):
        """
        Open file and get matching string based on regex

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
        """
        Replace all occurrences of string where is matched

        :rtype: self.replace_string returns True or False if the process found strings to replace
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

    def str_test_replace(self, file_input, str_old, str_new):
        for line in fileinput.input(file_input, inplace=True):
            if line:
                line = line.replace(str_old, str_new, line.rstrip())
                print(line)
                self.replace_string = True
            else:
                self.replace_string = False
        fileinput.close()
        return self.test
