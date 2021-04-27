# Setup
+ If you *want* automatic pdf scraping, you will need `wkhtmltopdf`
+ You will need the MOSS perl script in the **same directory** as `moss_util.py`
+ This script was tested on an Ubuntu virtual machine running on Windows Subsystem for Linux
+ This script assumes that your files are stored by directory, with the student identifier as the directory name.

# Usage

Maybe you just want a `.csv` file with all the student matches. Then, worry not!

## Want just the matches?

The use case below will output the top `n` rows from MOSS after accounting for the graph connectivity of students' work.

`python3 moss_util.py -b <path_to_base_file> -d "<dir_structure_for_moss>" -o <match_csv_fname> -n <num_matches>
`

Note the quotation marks around the `-d` flag, which seems to be necessary.

## Want pdf scraping?

Make sure that `wkhtmltopdf` is installed on your system. Take a look at the detailed flags breakdown by running:

`python3 moss_util.py -h`

The output is copied below:

```
usage: moss_util.py [-h] [--DEBUG] [-b BASE] [-d DIR] [-l LANG] [--pdf-save]
                    [--pdf-dir PDF_DIR] [-s PDF_SUFFIX] [-o OUT]
                    [-n NUM_STUDENTS] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --DEBUG               debug mode flag, likely unused
  -b BASE, --base BASE  moss base files
  -d DIR, --dir DIR     moss input files directory structure, relative
                        directories only
  -l LANG, --lang LANG  language, default Python
  --pdf-save            save flag, for saving pdf files from
                        the moss page
  --pdf-dir PDF_DIR     target output directory for pdf generation from moss,
                        relative directories only
  -s PDF_SUFFIX, --pdf-suffix PDF_SUFFIX
                        suffix for pdf files
  -o OUT, --out OUT     csv file to write matches to
  -n NUM_STUDENTS, --num-students NUM_STUDENTS
                        number of student matches to download
  -v, --verbose         verbosity flag
```
