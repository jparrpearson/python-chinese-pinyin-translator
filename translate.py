#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import getopt
import io
import os
import re
import shutil
import sys
import time

# TODO: Implement filename support (individual or in directory)

def main(argv):
    dictionaryFile = "resources/cedict_ts.u8"
    inputFile = ""
    inputDir = ""
    tones = False
    capitalize = True
    backup = True

    # Allow for unicode output to a non-unicode console
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding, errors="replace")

    # Get program arguments
    usage = "Example usage:\n  translate.py -h -f <file> -d <dir> -t <tones> -c <capitalize> -b <backup>"
    options = ("Options:\n  -h, --help - Shows the script usage and help options.\n"
        "  -f, --file - The input file to translate.  One of 'file' or 'dir' is required.\n"
        "  -d, --dir - The input directory to translate (translates all files in nested directories).  One of 'dir' or 'file' is required.\n"
        "  -t, --tones - Output the pinyin tone numbers.  Defaults to 'false'.\n"
        "  -c, --capitalize - Capitalize the pinyin (otherwise all lower case).  Defaults to 'true'.\n"
        "  -b, --backup - Backup each translated file ('filename.ext.BAK').  Defaults to 'true'.\n")
    try:
        opts, args = getopt.getopt(argv, "hf:d:t:c:b:", ["help", "file=", "dir=", "tones=", "capitalize=", "backup="])
    except getopt.GetoptError as err:
        print(str(er))
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(usage)
            print(options)
            sys.exit(0)
        elif opt in ("-f", "--file"):
            inputFile = arg
        elif opt in ("-d", "--dir"):
            inputDir = arg
        elif opt in ("-t", "--tones"):
            tones = True if arg.upper() == "TRUE" else False
        elif opt in ("-c", "--capitalize"):
            capitalize = True if arg.upper() == "TRUE" else False
        elif opt in ("-b", "--backup"):
            backup = True if arg.upper() == "TRUE" else False

    if not inputFile and not inputDir:
        print("Must provide either a file or directory to translate")
        print(usage)
        sys.exit(2)

    # Parse the dictionary file into a local dictionary
    start = time.time()
    global dict
    dict = {}
    with codecs.open(dictionaryFile, "r", encoding="utf-8") as file:
        pattern = "(.*?) (.*?) \[(.*?)\] /(.*?)/"
        for line in file:
            if not line.startswith('#') and not line.startswith('%'):
                match = re.match(pattern, line)
                if match:
                    pinyin = match.group(3)
                    pinyin = pinyin if tones else re.sub("[1234567890]", "", pinyin)
                    pinyin = pinyin.lower() if not capitalize else pinyin.capitalize()
                    # Add keys for traditional and simplified characters
                    dict[match.group(1)] = pinyin
                    dict[match.group(2)] = pinyin
    print("Loaded " + str(len(dict)) + " dictionary entries (" + getTime(start) + "s)")

    # Perform translation actions
    if inputFile:
        translateFile(inputFile, backup)
    elif inputDir:
        translateDir(inputDir, backup)

def translateFile(inputFile, backup):
    print("Translating file " + inputFile + "...")

    # Translate the file contents
    text = ""
    translated = False
    with codecs.open(inputFile, "r+", encoding="utf-8") as file:
        for line in file:
            for char in line:
                try:
                    value = dict[char]
                    if translated:
                        text += " "
                    text += value
                    translated = True
                except KeyError:
                    text += char
                    translated = False

        # Backup and write to disk
        if backup:
            filename = file.name + ".BAK"
            if not os.path.isfile(filename):
                print("Backing up to file " + filename)
                shutil.copy2(file.name, filename)
            else:
                print("Skipping backup to " + filename + " (file already exists)")
        file.seek(0)
        file.write(text)
        file.truncate()

def translateDir(inputDir, backup):
    print("Translating directory " + inputDir + "...")

    # Translate all nested files in the directory
    for subdir, dirs, files in os.walk(inputDir):
        for file in files:
            filename = os.path.join(subdir, file)
            if not filename.endswith(".BAK"):
                translateFile(filename, backup)

def getTime(start, digits=2):
    end = time.time()
    f = "{:." + str(digits) + "f}"
    return f.format(end-start)

if __name__ == "__main__":
    start = time.time()
    main(sys.argv[1:])
    print("Done (" + getTime(start) +"s)")
