#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import getopt
import hashlib
import sys

import numpy as np


def usage():
    print ""
    print "  Valid arguments are:"
    print ""
    print "    --big-kn   - run generator in big knowledge mode"
    print "    --debug    - run generator in debug mode"
    print "    --help     - show this message"
    print "    --out      - output file, default \"tests1.tst\""
    print "    --patterns - patterns file, default \"patterns1.pat\""
    print "    --rn       - file with random numbers, default \"rn1.txt\""
    print "    -b         - same as --big-kn"
    print "    -d         - same as --debug"
    print "    -h         - same as --help"
    print "    -o         - same as --out"
    print "    -p         - same as --patterns"
    print "    -r         - same as --rn"
    print ""


def generate_tests(debug, out, patterns_file, rn_file, big_kn):
    if debug:
        print "1. Loading random numbers from file."
    random_numbers = open_rn_file(rn_file)
    if debug:
        print "2. Load patterns from file."
    patterns = open_patterns_file(patterns_file)
    if debug:
        print "3. Prepare tests data."
    tests = []
    for iterator in range(len(random_numbers)):
        if big_kn:
            nbrnr = 6
        else:
            nbrnr = neighb_nr(random_numbers[(iterator+1) % len(random_numbers)])
        nbrs = neighbours(nbrnr,
                          alignment(random_numbers[(iterator+2) % len(random_numbers)]))
        tests.append(gen_test(patterns[random_numbers[iterator]], nbrs))
    if debug:
        print "4. Save tests file."
    save_tests(tests, out)


def open_rn_file(path):
    rns = []
    with open("./random_nrs/" + path) as text_file:
        for line in text_file:
            if len(line) > 0:
                new_number = line[:-1]
                rns.append(int(new_number))
    return rns


def open_patterns_file(path):
    patterns = []
    with open("./patterns/" + path) as text_file:
        for line in text_file:
            if len(line) > 0:
                patterns.append(line[:-1])
    return patterns


def save_tests(tests, dest_file):
    opened_file = codecs.open(dest_file, "w", "utf-8")
    for test in tests:
        opened_file.write(test + "\n")


def neighb_nr(random_from_0_to_255):
    # Can do %32, because they're uniform from [0, 255].
    random_for_neighb = random_from_0_to_255 % 32
    if random_for_neighb < 9:
        return 1
    elif random_for_neighb < 27:
        return 2
    elif random_for_neighb < 31:
        return 3
    return 4


def alignment(random_from_0_to_255):
    if random_from_0_to_255 > 251:
        np.random.seed(random_from_0_to_255)
        return np.random.randint(0, 6)
    # Otherwise can do %6, because they're uniform from [0, 251].
    return random_from_0_to_255 % 6


def neighbours(nr_of_them, start_align):
    def transform_nrs(number):
        return [1, 2, 3, 6, 5, 4][number]
    if nr_of_them == 1:
        return [start_align]
    ret_list = []
    for iterator in range(nr_of_them):
        ret_list.append(transform_nrs((start_align + iterator) % 6))
    return ret_list


def gen_test(random_pattern, neighbrs_list):
    test = ""
    for iterator in range(6):
        if iterator + 1 in neighbrs_list:
            test += random_pattern[iterator]
        else:
            test += 'N'
    test += 'N ' + random_pattern[6]
    # print random_pattern + "\t" + str(neighbrs_list) + "\t" + test
    return test


def main(argv):
    debug = False
    big_kn = False
    out = "tests1.tst"
    patterns_file = "patterns1.pat"
    rn_file = "rn1.txt"

    try:
        opts, _ = getopt.getopt(
            argv,
            "bdho:p:r:",
            ["help", "debug", "big-kn", "out=", "patterns=", "rn="]
        )
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            usage()
            sys.exit()
        elif opt in ('-b', "--big-kn"):
            big_kn = True
        elif opt in ('-d', "--debug"):
            debug = True
        elif opt in ('-o', "--out"):
            out = arg
        elif opt in ('-p', "--patterns"):
            patterns_file = arg
        elif opt in ('-r', "--rn"):
            rn_file = arg

    generate_tests(debug, out, patterns_file, rn_file, big_kn)


if __name__ == '__main__':
    main(sys.argv[1:])
