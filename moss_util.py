"""MOSS graph constructor to make matches more readable.

Identifies groups of matching solutions. This Python script MUST be in the
same directory as the moss perl script.
"""

import os
import requests
from datetime import datetime
import argparse


class Roster:
    def __init__(self) -> None:
        """ Initialize a record of students and matches

        students: List of Students
        size: int
        matches:
            List of List of int, an undirected graph. For each item
            in matches, the index <i> of item corresponds to the
            student at index <i> in students. The List of ints are the
            indices of the matching students.
        """
        self.students = []
        self.size = 0

        self.student_to_idx = {}
        self.matches = []
        self.student_to_idx = {}

    def add_student(self, new_student: str) -> None:
        """ Add a new student to the Roster
        """
        self.student_to_idx[new_student] = self.size  # update idx record
        self.students.append(new_student)  # update student record
        self.matches.append([])
        self.size += 1  # update size record

    def add_match(self, match1: str, match2: str) -> None:
        """ Update match records for both students.

        Note: This creates the full graph matrix.
        This can be made more efficient by just storing the
        "upper triangular" matrix of matches....
        """
        if match1 not in self.student_to_idx:  #  faster to look in keys than in list
            self.add_student(match1)
        if match2 not in self.student_to_idx:
            self.add_student(match2)

        idx1, idx2 = self.student_to_idx[match1], \
                     self.student_to_idx[match2]

        if idx2 not in self.matches[idx1]:
            self.matches[idx1].append(idx2)
        if idx1 not in self.matches[idx2]:
            self.matches[idx2].append(idx1)

    def __repr__(self) -> str:
        """ String representation of the Roster match matrix.
        """
        return '\n'.join(['\t'.join(
                [str(j)] + [str(i) for i in self.matches[j]]
            )
            for j in range(len(self.matches))]
        )


if __name__ == "__main__":
    time = datetime.now().strftime("%m%d%Y%H%M%S")

    parser = argparse.ArgumentParser()

    parser.add_argument("--DEBUG", action='store_true', default=False,
                        help="debug mode flag, likely unused")
    parser.add_argument("-b", "--base",
                        help="moss base files")
    parser.add_argument("-d", "--dir", default="./",
                        help="moss input files directory structure, relative directories only")
    parser.add_argument("-l", "--lang", default="python",
                        help="language, default Python")
    parser.add_argument("--pdf-save", default=False, action='store_true',
                        help="save flag, true or false, for saving pdf files from the moss page")  # default local
    parser.add_argument("--pdf-dir", default="./",
                        help="target output directory for pdf generation from moss, relative directories only")  # default local
    parser.add_argument("-s", "--pdf-suffix", default="",
                        help="suffix for pdf files")
    parser.add_argument("-o", "--out", default=f"./matches_{time}.csv",
                        help="csv file to write matches to")
    parser.add_argument("-n", "--num-students", default=50, type=int,
                        help="number of student matches to download")
    parser.add_argument("-v", "--verbose", default=False, action='store_true',
                        help="verbosity flag")

    args = parser.parse_args()

    if not args.DEBUG:
        print("Sending request to MOSS...")
        moss_cmd = f"./moss -l {args.lang} -b {args.base} -d {args.dir} | tail -1 > tmp.txt"  # grab the moss URL
        os.system(moss_cmd)
        print("MOSS response received")

        with open("./tmp.txt") as f:
            r = f.read().strip()
    else:
        print("Debug mode, no MOSS query attempted")
        r = ""  # hard coded MOSS URL here

    print(r)
    if not r.startswith("http"):
        print("MOSS terminated at:")
        print(r)
        raise Exception("MOSS script failed. Make sure your files exist.")

    roster = Roster()
    print("Finding matches...")
    for i in range(args.num_students):    # number of students
        last_utorid = ""
        for j in range(2):  # matches
            response = requests.get(r + "/match{}-{}.html".format(i, j))

            fname_start = response.text.find("<HR>")
            fname_end = response.text.find("<p>", fname_start)

            # print(response.text[fname_start + len("<TITLE>"):fname_end])  # not super robust
            utorid = response.text[fname_start + len("<TITLE>"):fname_end].rstrip("/")
            utorid = utorid[utorid.rfind("/") + 1:]

            if last_utorid != "":
                if args.verbose:
                    print("--- Match added ---")
                    print(utorid, last_utorid)
                roster.add_match(utorid, last_utorid)

            last_utorid = utorid
            fname = utorid + args.pdf_suffix + ".pdf"

            if args.verbose:
                print(f"{fname} saved to {args.pdf_dir}")

            if args.pdf_save:
                fout = os.path.join(args.pdf_dir, fname)
                cmd = "wkhtmltopdf " + r + "/match{}-{}.html ".format(i, j) + fout
                os.system(cmd)  # save the pdf

    if args.verbose:
        print("--- Matches stored found below ---")
        print(roster)

    # now save the match information
    # prune duplicates...

    print(f"Match finding complete, parsed {args.num_students} records and {roster.size} students")
    print("Writing the matches...")
    written = set()
    fout = open(f"./{args.out}", 'w')
    for i in range(roster.size):
        if i not in written:
            fout.write(roster.students[i] + ",")
            written.add(i)

            fout.write(','.join([roster.students[j] for j in roster.matches[i]]) + "\n")
            written.update([j for j in roster.matches[i]])

    fout.close()

    print("Utility completed, goodbye.")
