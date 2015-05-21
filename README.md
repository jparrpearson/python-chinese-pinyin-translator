# python-chinese-pinyin-translator

This is a Python script that translates Chinese characters (traditional or simplified) to Hanyu Pinyin.

The [CC-CEDICT dictionary](http://cc-cedict.org/wiki/) is used in translating.

## Usage

Translation can be applied to either a single file, all files in a directory (including nested directories).

For example, to translate a file `台灣.txt` in the `test` directory:
```
python translate.py -f test/台灣.txt
```

### Options

The following is a list of the possible options and their default values.

Note that `Short Name` parameters are specified with a single dash (e.g. `-h`), while `Long Name` parameters are specified with a double-dash (e.g. `--help`).

| Short Name | Long Name | Default | Description |
| --- | --- | --- |  --- |
| h | help | - | Shows the script usage and help options. |
| f | file | - | The input file to translate.  One of `file` or `dir` is required. |
| d | dir | - | The input directory to translate (translates all files in nested directories).  One of `dir` or `file` is required. |
| t | tones | false | Output the pinyin tone numbers. |
| c | capitalize | true | Capitalize the pinyin (otherwise all lower case). |
| b | backup | true | Backup each translated file (`filename.ext.BAK`). |

## License

Apache License, Version 2.0

Creative Commons Attribution-Share Alike 3.0 License (CC-CEDICT)