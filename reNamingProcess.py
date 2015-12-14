#!/usr/bin/python

import pprint
import subprocess
import stringManipulation


class RenamingProcess(object):
    """This class is for modifying the package name in the AndroidManifest.xml file
        and also the application name. e.g. application android:icon="@drawable/icon" android:label="new name"
        Secondly modifying all renaming all instances of main package."""

    def __init__(self, output=None):

        self.output = output
        """

        :rtype: object.output String with success or Error
        """

    def modification_process(self, app_section_name, data_conf_file):
        """Modify AndroidManifest.xml file"""
        # Instantiate object of the StringManipulationProcess class for AndroidManifest.xml
        manifest_xml_obj = stringManipulation.StringManipulationProcess()
        android_manifest_xml = manifest_xml_obj.get_android_manifest_xml(app_section_name)

        # Retrieve package PackageName from '*.ini' file
        key, new_package = data_conf_file[app_section_name][0]

        # Regex to modify package='com.something.something.etc'
        key += '=\"(.*?)\"'

        # Instantiate object of the StringManipulationProcess class for AndroidManifest.xml
        regex_xml_obj = stringManipulation.StringManipulationProcess()
        # Change applicationId to package name in build.gradle
        regex_package_name = regex_xml_obj.str_regex(android_manifest_xml, key, new_package)

        # Instantiate object of the StringManipulationProcess class
        replace_package_name_obj = stringManipulation.StringManipulationProcess()
        # Replace old package name in 'AndroidManifest.xml' file for all occurrences
        replace_package_name_obj.str_replace(android_manifest_xml, regex_package_name, new_package)

        """Modify build.gradle file"""
        


        # Instantiate object of the StringManipulationProcess class
        replace_package_build_gradle_obj = stringManipulation.StringManipulationProcess()
        # Replace old package name in 'AndroidManifest.xml' file for all occurrences
        replace_package_build_gradle_obj.str_replace(android_manifest_xml, regex_package_name, new_package)
        exit(1)

        # Retrieve package PackageName from '*.ini' file
        key, new_icon = data_conf_file[app_section_name][1]

        # Regex to modify android:icon="@mipmap/ic_launcher"
        key = 'android:' + key + '=' + '\"(.+?)\"'

        # Replace Android icon name in 'AndroidManifest.xml' file
        self.str_replace(android_manifest_xml, key, new_icon)

        # Replace Android Label name in 'strings.xml' file
        strings_xml = self.get_strings_xml(app_section_name)

        # Retrieve label android:label from '*.ini' file
        key, new_label = data_conf_file[app_section_name][2]

        # Regex to replace app_name label in
        key = '<string name=\"app_name\">.*</string>'
        # self.str_replace(android_manifest_xml, key, new_icon)
        #self.output = self.str_replace(strings_xml, key, new_label)

        return self.output
