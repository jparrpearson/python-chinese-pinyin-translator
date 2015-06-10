# python-chinese-pinyin-translator

This is a Python script that translates Chinese characters (traditional or simplified) to Hanyu Pinyin.

## Usage

Translation can be applied to either a single file, all files in a directory (including nested directories).  By default it translates just the file name, but it can also translate the file contents, or both filename and contents.

For example, to translate the file contents for a file named `test1.txt` in the `test` directory:
```
python translate.py -f test/test1.txt -p text
```

### Options

The following is a list of the possible options and their default values.

Note that `Short Name` parameters are specified with a single dash (e.g. `-h`), while `Long Name` parameters are specified with a double-dash (e.g. `--help`).

| Short Name | Long Name | Default | Description |
| --- | --- | --- |  --- |
| h | help | - | Shows the script usage and help options. |
| f | file | - | The input file to translate.  One of `file` or `dir` is required. |
| d | dir | - | The input directory to translate (translates all files in nested directories).  One of `dir` or `file` is required. |
| p | process | `filename` | Determines what is processed - `filename`, `text`, or `both`. |
| t | tones | `false` | Output the pinyin tone numbers. |
| c | capitalize | `true` | Capitalize the pinyin (otherwise all lower case). |
| b | backup | `true` | Backup each translated file (e.g. `filename.ext.BAK`). |

## License

Copyright 2015 Jeremy Parr-Pearson

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

--------------------------------------------------------------------------------

The following components are provided under the Creative Commons Attribution-ShareAlike 3.0 License.

CC-CEDICT Chinese English Dictionary - [http://cc-cedict.org/](http://cc-cedict.org/)
