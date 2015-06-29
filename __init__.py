#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import getopt
import hashlib
import sys

from hop_net import HopfieldNetwork


def usage():
    print ""
    print "  Valid arguments are:"
    print ""
    print "    --debug    - run generator in debug mode"
    print "    --help     - show this message"
    print "    --no-save  - don't save the results - only show them in console"
    print "    --out      - output file, default \"results.txt\""
    print "    --patterns - output file, default \"patternsT.pat\""
    print "    --prob     - prob mode - patterns are given in probabilities"
    print "    --seed     - seed for RNG"
    print "    --tests    - output file, default \"testsT.tst\""
    print "    -d         - same as --debug"
    print "    -h         - same as --help"
    print "    -n         - same as --no-save"
    print "    -o         - same as --out"
    print "    -p         - same as --patterns"
    print "    -s         - same as --seed"
    print "    -t         - same as --tests"
    print ""


def main(argv):
    debug = False
    save_res = True
    prob = False
    patterns_file = "patternsT.pat"
    tests_file = "testsT.tst"
    out = "results.txt"
    seed = None
    inputs_number = 98

    try:
        opts, _ = getopt.getopt(
            argv,
            "dhno:p:s:t:",
            ["help", "debug", "no-save", "out=", "patterns=", "prob", "seed=", "tests="]
        )
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            usage()
            sys.exit()
        elif opt in ('-d', "--debug"):
            debug = True
        elif opt in ('-n', "--no-save"):
            save_res = False
        elif opt in ('-o', "--out"):
            out = arg
        elif opt in ('-p', "--patterns"):
            patterns_file = arg
        elif opt in ("--prob"):
            prob = True
        elif opt in ('-s', "--seed"):
            seed = int(hashlib.sha1(arg).hexdigest(), 16) % 4294967295
        elif opt in ('-t', "--tests"):
            tests_file = arg

    HopfieldNetwork(inputs_number, patterns_file, tests_file, out, debug, save_res, seed, prob)


if __name__ == '__main__':
    main(sys.argv[1:])
