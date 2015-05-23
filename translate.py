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

def main(argv):
    # Defaults
    dictionaryFile = "resources/cedict_ts.u8"
    inputFile = ""
    inputDir = ""
    process = "filename"
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
        "  -p, --process - Determines what is processed - 'filename' (default), 'text', or 'both'.\n"
        "  -t, --tones - Output the pinyin tone numbers.  Defaults to 'false'.\n"
        "  -c, --capitalize - Capitalize the pinyin (otherwise all lower case).  Defaults to 'true'.\n"
        "  -b, --backup - Backup each translated file (e.g. 'filename.ext.BAK').  Defaults to 'true'.\n")
    try:
        opts, args = getopt.getopt(argv, "hf:d:p:t:c:b:", ["help", "file=", "dir=", "process=", "tones=", "capitalize=", "backup="])
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
        elif opt in ("-p", "--process"):
            if arg not in ("filename", "text", "both"):
                print("Invalid process option")
                print(usage)
                sys.exit(2)
            process = arg
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
    dict = {}
    with codecs.open(dictionaryFile, "r", encoding="utf-8") as file:
        pattern = "(.*?) (.*?) \[(.*?)\] /(.*?)/"
        for line in file:
            if not line.startswith('#') and not line.startswith('%'):
                match = re.match(pattern, line)
                if match:
                    pinyin = match.group(3)
                    # Determine tone numbers and capitalization
                    pinyin = pinyin if tones else re.sub("[1234567890]", "", pinyin)
                    pinyin = pinyin.lower() if not capitalize else pinyin.capitalize()
                    # Add keys for traditional and simplified characters
                    dict[match.group(1)] = pinyin
                    dict[match.group(2)] = pinyin
    print("Loaded " + str(len(dict)) + " dictionary entries (" + getTime(start) + "s)")

    # Perform translation actions
    if inputFile:
        translateFile(inputFile, dict, process, backup)
    elif inputDir:
        count = translateDir(inputDir, dict, process, backup)
        print("Translated " + str(count) + " files")

def translateFile(inputFile, dict, process, backup):
    """Translates the file (filename, text, or both)."""
    print("Translating file " + inputFile + "...")

    # Translate the file contents
    with codecs.open(inputFile, "r+", encoding="utf-8") as file:
        # Backup the file
        if backup:
            filename = file.name + ".BAK"
            if not os.path.isfile(filename):
                print("Backing up to file " + filename)
                shutil.copy2(file.name, filename)
            else:
                print("Skipping backup to " + filename + " (file already exists)")

        # Translate the file contents (text)
        if process in ("text", "both"):
            text = ""
            for line in file:
                text += translateLine(line, dict)
            file.seek(0)
            file.write(text)
            file.truncate()

        # Translate the filename
        if process in ("filename", "both"):
            filename = translateLine(file.name, dict)
            file.close()
            print("Changing filename to " + filename)
            os.rename(file.name, filename)

def translateDir(inputDir, dict, process, backup):
    """Translates all files in the given directory, and all nested directories.  Returns the number of files translated."""
    print("Translating directory " + inputDir + "...")

    # Translate all nested files in the directory
    count = 0
    for subdir, dirs, files in os.walk(inputDir):
        for file in files:
            filename = os.path.join(subdir, file)
            if not filename.endswith(".BAK"):
                translateFile(filename, dict, process, backup)
                count += 1
    return count

def translateLine(line, dict):
    """Translates and returns a given line of text."""
    text = ""
    translated = False
    for char in line:
        # Use the matching value in the dictionary, otherwise output the existing character
        try:
            value = dict[char]
            if translated:
                text += " "
            text += value
            translated = True
        except KeyError:
            text += char
            translated = False
    return text

def getTime(start, digits=2):
    """Get and return the time elapsed since start to now (in seconds, to digits decimal places)."""
    end = time.time()
    f = "{:." + str(digits) + "f}"
    return f.format(end-start)

if __name__ == "__main__":
    start = time.time()
    main(sys.argv[1:])
    print("Done (" + getTime(start) +"s)")
