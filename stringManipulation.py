#!/usr/bin/python

import os
import re
import fileinput
import subprocess


class StringManipulationProcess(object):
    """This class is for manipulating string(s) necessary for our purposes."""

    def __init__(self,
                 output=None,
                 move_dir=None,
                 working_dir=None,
                 file_output=None,
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
        self.move_dir = move_dir
        self.working_dir = working_dir
        self.file_output = file_output
        self.strings_file = strings_file
        self.regex_string = regex_string
        self.build_gradle = build_gradle
        self.replace_string = replace_string
        self.bash_cmd_return = bash_cmd_return
        self.list_package_name = list_package_name
        self.gradlew_std_output = gradlew_std_output
        self.android_manifest_file = android_manifest_file

    def find_file(self, file_name, path):
        working_directory = self.get_working_directory()
        path = working_directory + path
        for root, dirs, files in os.walk(path):
            if file_name in files:
                self.file_output = os.path.join(root, file_name)
                return self.file_output
            else:
                self.file_output = False
                return self.file_output

    def get_working_directory(self):
        """
        Obtain the current directory else raise error

        :rtype: Raise error in case the current directory can not be retrieved
        """
        try:
            self.working_dir = os.getcwd()
        except OSError as e:
            self.working_dir = e.self.working_dir
            print "Error: {}".format(self.working_dir)
        return self.working_dir

    def move_to_directory(self, path):
        """
        Trying to move to the specified path else raise error

        :rtype: True or False based on output
        """
        try:
            os.chdir(path)
            self.move_dir = True
        except OSError:
            print "Could not enter: {} to build the module".format(path)
            self.move_dir = False
        return self.move_dir

    def compile_and_build_project(self, app_section):

        working_directory = self.get_working_directory()

        # Change directory to build the cloned app
        path = working_directory + "/" + app_section

        self.move_to_directory(path)

        build_std_out = self.execute_bash_cmd('./gradlew build')

        if "BUILD SUCCESSFUL" not in build_std_out:
            self.gradlew_std_output = False
        else:
            self.gradlew_std_output = True

        self.move_to_directory(working_directory)

        return self.gradlew_std_output

    def get_list_of_package_name_files(self, app_section):
        """
        list all occurrences of 'package=what.ever.here'. We do not care about debug 'package=etc' because it will
        reproduce the files for us automatically when we will compile the app by running ./gradlew build

        :param app_section: Each directory has a different section name to use for each clone
        """

        working_directory = self.get_working_directory()
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

        working_directory = self.get_working_directory()
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
        except subprocess.CalledProcessError as e:
            self.bash_cmd_return = e
        return self.bash_cmd_return

    def get_strings_xml(self, app_section):
        """
        Get path for strings.xml file

        :rtype: Path to the specified strings.xml file based on section of configuration.ini file
        :type app_section: Each directory has a different section name to use for each clone
        """

        working_directory = self.get_working_directory()
        self.strings_file = working_directory + "/" + app_section + "/app/src/main/res/values/strings.xml"
        return self.strings_file

    def get_build_gradle_app(self, app_section):
        """
        Get path for build.gradle file

        :param app_section: Each directory has a different section name to use for each clone
        :rtype: Path to the specified builde.gradle file based on section of configuration.ini file
        """

        working_directory = self.get_working_directory()
        self.build_gradle = working_directory + "/" + app_section + "/app/build.gradle"
        return self.build_gradle

    def str_regex(self, file_input, regex_key):
        """
        Open file and get matching string based on regex

        :param regex_key: Find all occurrences based on regex input
        :param file_input: File input to use regex
        :rtype: self.regex_string returns string matched based on regex
        """
        try:
            with open(file_input, "r") as fr:
                str_data = fr.read()
                str_line = re.findall(r'{}'.format(regex_key), str_data)
        except IOError as e:
            print(e)
            exit(1)
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
