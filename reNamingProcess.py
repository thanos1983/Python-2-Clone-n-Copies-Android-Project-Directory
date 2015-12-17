#!/usr/bin/python

import pprint
import subprocess
import stringManipulation


class RenamingProcess(object):
    """
    This class is used to modify the package name in the AndroidManifest.xml file,
    also the application name. e.g. application android:icon="@drawable/icon" android:label="new name"
    also modifying the app_name in strings.xml file e.g. <string name="app_name">New Name</string>
    also modifying all remaining instances of main package.

    :rtype: object.output returns True or False
    """

    def __init__(self,
                 icon=None,
                 gradle=None,
                 output=None,
                 strings=None,
                 package=None,
                 file_data=None,
                 android_manifest_data=None):

        self.icon = icon
        self.gradle = gradle
        self.output = output
        self.strings = strings
        self.package = package
        self.file_data = file_data
        self.android_manifest_data = android_manifest_data

    def modification_process(self, app_section_name, conf_file):
        """
        Modify AndroidManifest.xml, build.gradle and Strings.xml file(s)

        :param conf_file: The file contains all clones data that we want to modify (package, icon, app_name)
        :param app_section_name: Each directory has a different section name to use for each clone
        """

        return_package_name = self.modify_package_name(app_section_name, conf_file)
        return_android_icon = self.modification_android_icon(app_section_name, conf_file)
        return_strings_xml = self.modification_strings_xml_file(app_section_name, conf_file)

        gradlew_build_obj = stringManipulation.StringManipulationProcess()
        gradlew_build_std_output = gradlew_build_obj.compile_and_build_project(app_section_name)

        if return_package_name is True and return_android_icon is True and \
                return_strings_xml is True and gradlew_build_std_output is True:

            self.output = True
        else:
            self.output = False
        return self.output

    def retrieve_data_android_manifest_file(self, app_section_name, conf_file):
        """
        Extract all the data from the AndroidManifest.xml file e.g. 'package="com.something.something.etc"'

        :type app_section_name: string
        :type conf_file: dictionary with lists
        """
        manifest_xml_obj = stringManipulation.StringManipulationProcess()
        android_manifest_xml_file = manifest_xml_obj.get_android_manifest_xml(app_section_name)

        # Retrieve package PackageName from '*.ini' file
        key, new_package_name = conf_file[app_section_name][0]

        regex_key = key + '=\"(.*?)\"'
        # Regex to modify package='com.something.something.etc'
        key += regex_key

        # Instantiate object of the StringManipulationProcess class for file input
        regex_xml_obj = stringManipulation.StringManipulationProcess()

        # Retrieve matched string based on file and regex input
        old_package_name = regex_xml_obj.str_regex(android_manifest_xml_file, regex_key)

        self.android_manifest_data = android_manifest_xml_file, old_package_name, new_package_name
        return self.android_manifest_data

    def modify_package_name(self, app_section_name, conf_file):
        """
        Modifying package="com.something.etc" to the desired name from configuration file

        :param conf_file: The file contains all clones data that we want to modify (package, icon, app_name)
        :param app_section_name: Each directory has a different section name to use for each clone
        """
        android_manifest_xml_package_name_old_new = self.retrieve_data_android_manifest_file(app_section_name,
                                                                                             conf_file)

        # Instantiate object of the StringManipulationProcess class
        list_package_name_files_obj = stringManipulation.StringManipulationProcess()
        list_package_name_files = list_package_name_files_obj.get_list_of_package_name_files(app_section_name)

        # Check if this app contains the gcm file 'google-services.json'
        path = "/" + app_section_name + "/app/"
        # Instantiate object of the StringManipulationProcess class
        find_file_obj = stringManipulation.StringManipulationProcess()
        find_file_return_value = find_file_obj.find_file('google-services.json', path)

        if find_file_return_value:
            list_package_name_files.append(find_file_return_value)

        # Instantiate object of the StringManipulationProcess class
        replace_package_name_obj = stringManipulation.StringManipulationProcess()
        # Replace old package name in all file(s) for all occurrences
        for file_element in list_package_name_files:
            self.package = replace_package_name_obj.str_replace(file_element,
                                                                android_manifest_xml_package_name_old_new[1],
                                                                android_manifest_xml_package_name_old_new[2])

        self.modify_gradle_file(app_section_name,
                                android_manifest_xml_package_name_old_new[1],
                                android_manifest_xml_package_name_old_new[2])

        return self.package

    def modify_gradle_file(self, app_section_name, old_package_name, new_package_name):
        """
        Modify build.gradle file

        :param new_package_name: Name retrieved from configurationFile.ini based on section
        :param old_package_name: Name retrieved initially from AndroidManifest.xml file
        :param app_section_name: Each directory has a different section name to use for each clone
        """

        build_gradle_file_obj = stringManipulation.StringManipulationProcess()
        # Retrieve build.gradle file path
        build_gradle_file = build_gradle_file_obj.get_build_gradle_app(app_section_name)

        # Instantiate object of the StringManipulationProcess class
        replace_package_build_gradle_obj = stringManipulation.StringManipulationProcess()
        # Replace old package name in 'build.gradle' file for all occurrences
        self.gradle = replace_package_build_gradle_obj.str_replace(build_gradle_file,
                                                                   old_package_name,
                                                                   new_package_name)
        return self.gradle

    def modification_android_icon(self, app_section_name, conf_file):
        """
        Modifying android:icon="@mipmap/ic_launcher" to the desired icon from configuration file

        :param conf_file: The file contains all clones data that we want to modify (package, icon, app_name)
        :param app_section_name: Each directory has a different section name to use for each clone
        """
        manifest_xml_obj = stringManipulation.StringManipulationProcess()
        android_manifest_xml_file = manifest_xml_obj.get_android_manifest_xml(app_section_name)

        # Retrieve package PackageName from '*.ini' file
        key, new_icon = conf_file[app_section_name][1]

        # Regex to modify android:icon="@mipmap/ic_launcher"
        key = 'android:' + key + '=' + '\"(.+?)\"'

        regex_android_icon_obj = stringManipulation.StringManipulationProcess()
        # Change android:icon to icon name in AndroidManifest.xml
        regex_icon_name = regex_android_icon_obj.str_regex(android_manifest_xml_file, key)

        # Instantiate object of the StringManipulationProcess class
        android_icon_obj = stringManipulation.StringManipulationProcess()
        # Replace Android icon name in 'AndroidManifest.xml' file
        self.icon = android_icon_obj.str_replace(android_manifest_xml_file, regex_icon_name, new_icon)
        return self.icon

    def modification_strings_xml_file(self, app_section_name, conf_file):
        """
        Modifying 'Strings.xml' file for the app_name attribute

        :param conf_file: The file contains all clones data that we want to modify (package, icon, app_name)
        :param app_section_name: Each directory has a different section name to use for each clone
        :rtype: self.strings returns True or False depends upon the process
        """
        # Instantiate object of the StringManipulationProcess class
        strings_xml_obj = stringManipulation.StringManipulationProcess()
        # Replace Android Label name in 'strings.xml' file
        strings_xml = strings_xml_obj.get_strings_xml(app_section_name)

        # Retrieve label android:label from '*.ini' file
        key, new_label = conf_file[app_section_name][2]

        # Regex to replace app_name label in
        key = '<string name=\"app_name\">.*</string>'

        # Instantiate object of the StringManipulationProcess class
        regex_strings_obj = stringManipulation.StringManipulationProcess()
        # Change applicationId to package name in build.gradle
        regex_app_name = regex_strings_obj.str_regex(strings_xml, key)

        # Instantiate object of the StringManipulationProcess class
        replace_app_name_obj = stringManipulation.StringManipulationProcess()
        # Replace old app_name in 'Strings.xml' file

        self.strings = replace_app_name_obj.str_replace(strings_xml, regex_app_name, new_label)
        return self.strings
