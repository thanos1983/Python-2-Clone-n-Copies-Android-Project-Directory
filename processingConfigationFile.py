#!/usr/bin/python

import ConfigParser


class ConfigurationFileProcess(object):
    """Class processing configuration file.
        Load all section necessary for creation of the App"""

    def __init__(self, apps_data_out=None, source_app=None):

        self.source_app = source_app
        self.apps_data_out = apps_data_out

    def process_conf_file(self, conf_file):

        # Instantiate object of the ConfigParser class
        """

        :rtype: Data for each app, and source file
        """
        parser_obj = ConfigParser.ConfigParser()
        # Read the specified configuration file
        parser_obj.read(conf_file)

        # Extract all Apps to be created
        list_of_sections = parser_obj.sections()

        self.source_app = list_of_sections[0]

        # remove Template no need to be processed.
        del list_of_sections[0]

        dictionary = {}
        for section_name in list_of_sections:
            dictionary[section_name] = parser_obj.items(section_name)

        self.apps_data_out = dictionary

        return self.apps_data_out, self.source_app
