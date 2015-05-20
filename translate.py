#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import io
import getopt
import codecs
import re
import os
import shutil

# TODO: Add timing information (dictionary load and for each file translation)
# TODO: Implement filename support (individual or in directory)
# TODO: Add information on parameters (part of usage)

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
    usage = "translate.py -h -f <file> -d <dir> -t <tones> -c <capitalize> -b <backup>"
    try:
        opts, args = getopt.getopt(argv, "hf:d:t:c:b:", ["help", "file=", "dir=", "tones=", "capitalize=", "backup="])
    except getopt.GetoptError as err:
        print(str(er))
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(usage)
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

    # Parse the dictionary file into a local dictionary
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
    print("Loaded " + str(len(dict)) + " dictionary entries")

    # Perform translation actions
    if inputFile:
        translateFile(inputFile, backup)
    elif inputDir:
        translateDir(inputDir, backup)
    else:
        print("Must provide either a file or directory to translate")
        print(usage)

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

if __name__ == "__main__":
    main(sys.argv[1:])
    print("Done")
