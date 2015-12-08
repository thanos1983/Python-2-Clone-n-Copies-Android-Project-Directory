#!/usr/bin/python

import sys
import cloningProcess

if __name__ == '__main__':

    if len(sys.argv) != 4:
        print "Usage: python {} [Android App Dir. SRC] [Number of Copies] [Android App Dir. DST]".format(sys.argv[0])
        sys.exit(1)
    elif not sys.argv[2].isdigit():
        print "Please enter a valid number of copies"
        sys.exit(1)

    sys.argv[3] = sys.argv[3].translate(None, '/')

    process_obj = cloningProcess.DuplicationProcess()  # Instantiate object of the DuplicationProcess class

    output_dictionary = {}

    for i in range(int(sys.argv[2])):
        output_dictionary[sys.argv[3] + '{}'.format(i)] = process_obj.clone(sys.argv[1], sys.argv[3] + '{}'.format(i))

    print output_dictionary
