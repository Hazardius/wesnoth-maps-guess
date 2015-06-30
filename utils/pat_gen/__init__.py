#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import getopt
import hashlib
import sys


def usage():
    print ""
    print "  Valid arguments are:"
    print ""
    print "    --cons     - run generator in consolidate patterns mode"
    print "    --count    - run generator in count terrains mode"
    print "    --debug    - run generator in debug mode"
    print "    --help     - show this message"
    print "    --map      - map file, default \"test.map\""
    print "    --out      - output file, default \"patternsT.pat\""
    print "    --rn       - file with random numbers, default \"rnT.txt\""
    print "    -c         - same as --cons"
    print "    -d         - same as --debug"
    print "    -h         - same as --help"
    print "    -m         - same as --map"
    print "    -o         - same as --out"
    print "    -r         - same as --rn"
    print ""


def generate_patterns(debug=False,
                      map_file="test.map",
                      out="patternsT.pat",
                      rn_file="rnT.txt"):
    if debug:
        print "1. Loading random numbers from file."
    random_numbers = open_rn_file(rn_file)
    if debug:
        print "2. Load map data from file."
    processed_map = open_map_file(map_file)
    if debug:
        print "3. Prepare patterns data."
    (patterns, prob_patterns) = get_patterns(processed_map, random_numbers)
    if debug:
        print "4. Save patterns files."
    save_patterns(patterns, prob_patterns, out)

def consolidate_patterns(debug=False, out="patternsT.pat"):
    if debug:
        print "1. Loading patterns from file and calculating probabilistic patterns."
    prob_pat = open_patterns_file(out)
    if debug:
        print "2. Save probabilistic patterns file."
    save_consolidated_patterns(prob_pat, out)

def count_terrains(debug=False, out="patternsT.pat"):
    def letter(index):
        return "ACDGHIKMQRSUWXN"[index]
    if debug:
        print "1. Loading patterns from file."
    letters_counter = [0 for _ in range(14)]
    with open("./patterns/" + out) as text_file:
        for line in text_file:
            pattern = line[:-1]
            for character in pattern:
                letters_counter[letter_to_number(character)] += 1
    if debug:
        print "2. Printing the results."
    all_tiles = sum(letters_counter)
    for iterator in range(14):
        print (letter(iterator) + "\t" + str(letters_counter[iterator]) + "\t" +
               str(100.0*letters_counter[iterator]/all_tiles))
    print "Sum\t" + str(all_tiles)

def open_rn_file(path):
    rns = []
    with open("./random_nrs/" + path) as text_file:
        for line in text_file:
            new_pair = line[:-1].split()
            rns.append((int(new_pair[0]), int(new_pair[1])))
    return rns


def open_map_file(path):
    ret_map = []
    with open("./maps/" + path) as text_file:
        for line in text_file:
            map_line = []
            raw_line = line[:-1].split(', ')
            for element in raw_line:
                if element[0].isdigit():
                    map_line.append(element[2])
                else:
                    map_line.append(element[0])
            ret_map.append(map_line)
    return ret_map


def open_patterns_file(path):

    def num2letter(index):
        return "ACDGHIKMQRSUWXN"[index]

    prob_patterns = [[[0 for _ in range(14)] for _ in range(6)] for _ in range(14)]
    with open("./patterns/" + path) as text_file:
        for line in text_file:
            pattern = line[:-1]
            letter = letter_to_number(pattern[-1])
            mini_iter = 0
            for nlet in pattern[:-1]:
                prob_patterns[letter][mini_iter][letter_to_number(nlet)] += 1
                mini_iter += 1
    nprob_patterns = []
    letter_id = 0
    for row in prob_patterns:
        is_valid_pattern = True
        one_set = []
        for neighbr in row:
            nsum = sum(neighbr)
            if nsum == 0:
                is_valid_pattern = False
                break
            else:
                max_id = 0
                max_val = 0
                for candidate in range(14):
                    if max_val < neighbr[candidate]:
                        max_id = candidate
                        max_val = neighbr[candidate]
                one_set.append(num2letter(max_id))
                # Old version:
                # multiplier = 1.0 / max(neighbr)
                # one_set.append([((neighbr[i] * multiplier)/nsum - 0.0) for i in range(14)])
        one_set.append(num2letter(letter_id))
        letter_id += 1
        if not is_valid_pattern:
            continue
        nprob_patterns.append(one_set)
    return nprob_patterns


def save_patterns(patterns, prob_patterns, dest_file):
    opened_file = codecs.open(dest_file, "w", "utf-8")
    for pattern in patterns:
        opened_file.write(pattern + "\n")
    opened_file = codecs.open((dest_file + "prob"), "w", "utf-8")
    iterator = 0
    for pattern in prob_patterns:
        line = ""
        for field in pattern:
            for prob in field:
                line += str(prob) + " "
        for sec_iter in range(14):
            if sec_iter != iterator:
                line += str(-1.0) + " "
            else:
                line += str(1.0) + " "
        line = line[:-1] + '\n'
        opened_file.write(line)
        iterator += 1


def save_consolidated_patterns(prob_pat, dest_file):
    opened_file = codecs.open((dest_file + "prob"), "w", "utf-8")
    for pattern in prob_pat:
        patternasastring = ''.join(pattern)
        opened_file.write(patternasastring + "\n")
    # Old version
    # iterator = 0
    # for pattern in prob_pat:
    #     line = ""
    #     for field in pattern:
    #         for prob in field:
    #             line += str(prob) + " "
    #     for sec_iter in range(14):
    #         if sec_iter != iterator:
    #             line += str(-1.0) + " "
    #         else:
    #             line += str(1.0) + " "
    #     line = line[:-1] + '\n'
    #     opened_file.write(line)
    #     iterator += 1


def letter_to_number(letter):
    return {
        'A': 0,
        'C': 1,
        'D': 2,
        'G': 3,
        'H': 4,
        'I': 5,
        'K': 6,
        'M': 7,
        'Q': 8,
        'R': 9,
        'S': 10,
        'U': 11,
        'W': 12,
        'X': 13,
    }[letter]


def get_neighbourhood(x, y):
    neighbourhood = []
    if x%2 == 0:
        neighbourhood.append((x-1, y))
    else:
        neighbourhood.append((x-1, y-1))
    neighbourhood.append((x, y-1))
    if x%2 == 0:
        neighbourhood.append((x+1, y))
        neighbourhood.append((x-1, y+1))
    else:
        neighbourhood.append((x+1, y-1))
        neighbourhood.append((x-1, y))
    neighbourhood.append((x, y+1))
    if x%2 == 0:
        neighbourhood.append((x+1, y+1))
    else:
        neighbourhood.append((x+1, y))
    neighbourhood.append((x, y))
    return neighbourhood


def get_patterns(processed_map, random_numbers):
    patterns = []
    prob_patterns = [[[0 for _ in range(14)] for _ in range(6)] for _ in range(14)]
    for (x, y) in random_numbers:
        pattern = ""
        letter = ''
        neighb = get_neighbourhood(x, y)
        for (a, b) in neighb:
            letter = processed_map[a][b]
            pattern += letter
        letter = letter_to_number(letter)
        mini_iter = 0
        for nlet in pattern[:-1]:
            prob_patterns[letter][mini_iter][letter_to_number(nlet)] += 1
            mini_iter += 1
        patterns.append(pattern)
    nprob_patterns = []
    for row in prob_patterns:
        one_set = []
        for neighbr in row:
            nsum = sum(neighbr)
            if nsum == 0:
                one_set.append([-0.5 for _ in range(14)])
            else:
                multiplier = 2.0 / max(neighbr)
                one_set.append([((neighbr[i] * multiplier) - 1.0) for i in range(14)])
        nprob_patterns.append(one_set)
    return (patterns, nprob_patterns)


def main(argv):
    consolidate = False
    count = False
    debug = False
    map_file = "test.map"
    out = "patternsT.pat"
    rn_file = "rnT.txt"

    try:
        opts, _ = getopt.getopt(
            argv,
            "cdhm:o:r:",
            ["help", "cons", "count", "debug", "map=", "out=", "rn="]
        )
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            usage()
            sys.exit()
        elif opt in ('-c', "--cons"):
            consolidate = True
        elif opt in ("--count"):
            count = True
        elif opt in ('-d', "--debug"):
            debug = True
        elif opt in ('-m', "--map"):
            map_file = arg
        elif opt in ('-o', "--out"):
            out = arg
        elif opt in ('-r', "--rn"):
            rn_file = arg

    if count:
        count_terrains(debug, out)
    elif consolidate:
        consolidate_patterns(debug, out)
    else:
        generate_patterns(debug, map_file, out, rn_file)


if __name__ == '__main__':
    main(sys.argv[1:])
