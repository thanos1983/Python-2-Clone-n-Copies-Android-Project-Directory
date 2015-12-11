#!/usr/bin/python

import sys
import pprint
import cloningProcess
import reNamingProcess
import configurationFileProcess

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "Usage: python {} [Android App Dir. SRC] [Configuration File]".format(sys.argv[0])
        sys.exit(1)
    elif ".ini" not in sys.argv[2]:
        print "Usage: python {} [Android App Dir. SRC] [Configuration File.ini]".format(sys.argv[0],
                                                                                        sys.argv[2])
        sys.exit(1)

    conf_file_obj = configurationFileProcess.ConfigurationFileProcess()
    data_conf_file, source_file = conf_file_obj.process_conf_file(sys.argv[2])

    # pprint.pprint(data_conf_file)

    app_names_list = data_conf_file.keys()
    number_of_clones = len(app_names_list)

    cloning_obj = cloningProcess.DuplicationProcess()  # Instantiate object of the DuplicationProcess class
    renaming_obj = reNamingProcess.RenamingProcess()  # Instantiate object of the DuplicationProcess class

    cloning_dictionary = {}
    for i in range(int(number_of_clones)):
        cloning_dictionary[app_names_list[i]] = cloning_obj.clone(source_file, app_names_list[i])
        renaming = renaming_obj.modification_process(app_names_list[i], data_conf_file)
    # print renaming
    exit(0)
