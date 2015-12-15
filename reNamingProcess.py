#!/usr/bin/python

import pprint
import subprocess
import stringManipulation


class RenamingProcess(object):
    """This class is for modifying the package name in the AndroidManifest.xml file
        and also the application name. e.g. application android:icon="@drawable/icon" android:label="new name"
        Secondly modifying all renaming all instances of main package."""

    def __init__(self, icon=None, gradle=None, package=None, file_data=None, android_manifest=None):
        self.icon = icon
        self.gradle = gradle
        self.package = package
        self.file_data = file_data
        self.android_manifest = android_manifest

        """
        :rtype: object.output String with success or Error
        """

    def retrieve_data_from_file(self, app_section_name, conf_file, regex_key, specified_file):
        """Retrieving data from AndroidManifest.xml file based on regex

        :rtype: file_data: Returns the matched strings based on the file and regex provided
        :param specified_file: Input file to retrieve data e.g. (AndroidManifest.xml, builde.gradle, etc)
        :param regex_key: Regex to search file for the matching string
        :param app_section_name: Each directory has a different section name to use for each clone
        :param conf_file: The file contains all clones data that we want to modify (package, icon, app_name)
        """

        # Instantiate object of the StringManipulationProcess class for AndroidManifest.xml
        regex_xml_obj = stringManipulation.StringManipulationProcess()
        # Change applicationId to package name in build.gradle
        regex_package_name = regex_xml_obj.str_regex(specified_file, key)
        self.file_data = regex_package_name, new_package
        return self.file_data

    def retrieve_data_android_manifest_file(self, app_section_name, conf_file):
        # Instantiate object of the StringManipulationProcess class for AndroidManifest.xml
        manifest_xml_obj = stringManipulation.StringManipulationProcess()
        android_manifest_xml_file = manifest_xml_obj.get_android_manifest_xml(app_section_name)

        # Retrieve package PackageName from '*.ini' file
        key, new_package = conf_file[app_section_name][0]

        regex_key = '=\"(.*?)\"'
        # Regex to modify package='com.something.something.etc'
        key += regex_key
        self.android_manifest = self.retrieve_data_from_file(app_section_name,
                                                             conf_file,
                                                             regex_key,
                                                             android_manifest_xml_file)
        print "Android Manifest: {}" .format(self.android_manifest)
        exit(1)
        return self.android_manifest

    def modify_package_name(self, app_section_name, conf_file):
        """Modifying package="com.something.etc" to the desired name from configuration file

        :param conf_file: The file contains all clones data that we want to modify (package, icon, app_name)
        :param app_section_name: Each directory has a different section name to use for each clone
        """
        android_manifest_xml = self.retrieve_data_android_manifest_file(app_section_name, conf_file)

        # Instantiate object of the StringManipulationProcess class
        replace_package_name_obj = stringManipulation.StringManipulationProcess()
        # Replace old package name in 'AndroidManifest.xml' file for all occurrences
        self.package = replace_package_name_obj.str_replace(android_manifest_xml_file,
                                                            android_manifest_xml[0],
                                                            android_manifest_xml[1])
        return self.package

    def modify_gradle_file(self, app_section_name, conf_file):
        """Modify build.gradle file

        :param conf_file: configuration.ini file, retrieve data based on key
        :param app_section_name: Each directory has a different section name to use for each clone
        """

        build_gradle_file_obj = stringManipulation.StringManipulationProcess()
        # Retrieve build.gradle file path
        build_gradle_file = build_gradle_file_obj.get_build_gradle_app(app_section_name)

        regex_key = '=\"(.*?)\"'
        file_data = self.retrieve_data_from_file(app_section_name,
                                                 conf_file,
                                                 regex_key,
                                                 build_gradle_file)
        exit(1)

        # Instantiate object of the StringManipulationProcess class
        replace_package_build_gradle_obj = stringManipulation.StringManipulationProcess()
        # Replace old package name in 'build.gradle' file for all occurrences
        self.gradle = replace_package_build_gradle_obj.str_replace(build_gradle_file,
                                                                   file_data[0],
                                                                   file_data[1])
        print "Return: {}".format(self.gradle)
        return self.gradle

    def modification_process(self, app_section_name, conf_file):
        """Modify AndroidManifest.xml, build.gradle and Strings.xml file(s)

        :param conf_file: The file contains all clones data that we want to modify (package, icon, app_name)
        :param app_section_name: Each directory has a different section name to use for each clone
        """

        self.modify_package_name(app_section_name, conf_file)
        self.modify_gradle_file(app_section_name, conf_file)
        exit(1)

        """Modifying android:icon="@mipmap/ic_launcher" to the desired icon from configuration file"""
        # Retrieve package PackageName from '*.ini' file
        key, new_icon = conf_file[app_section_name][1]

        # Regex to modify android:icon="@mipmap/ic_launcher"
        key = 'android:' + key + '=' + '\"(.+?)\"'

        regex_android_icon_obj = stringManipulation.StringManipulationProcess()
        # Change android:icon to icon name in AndroidManifest.xml
        regex_icon_name = regex_android_icon_obj.str_regex(android_manifest_xml, key, )

        # Instantiate object of the StringManipulationProcess class
        android_icon_obj = stringManipulation.StringManipulationProcess()
        # Replace Android icon name in 'AndroidManifest.xml' file
        android_icon_obj.str_replace(android_manifest_xml, regex_icon_name, new_icon)

        """Modifying 'Strings.xml' file for the app_name attribute"""
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
        replace_app_name_obj.str_replace(strings_xml, regex_app_name, new_label)

        return self.output
