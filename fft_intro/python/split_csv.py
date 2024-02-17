#!/usr/bin/python

import sys

from typing import List

def get_ofilename(filename: str, fcount: int) -> str:
    return "{}_{}.csv".format(filename.split(".")[0], fcount)


def split(filename: str, filesize: int) -> None:
    fcount = 0 # File count.
    ln = 0     # Line number.
    fpr = open(filename, "r") # File pointer to read.
    ofile = get_ofilename(filename, fcount)
    fpw = open(get_ofilename(filename, fcount), "w") # File pointer to write.

    for line in fpr:
        ln += 1
        if ln > filesize:
            ln = 1
            fpw.close()
            fcount += 1
            fpw = open(get_ofilename(filename, fcount), "w")

        fpw.write(line)

    fpr.close()


def main(argv: List[str]) -> None:
    if len(argv) == 3:
        fname = argv[1]
        filesize = int(argv[2])
        split(fname, filesize)
        sys.exit(0)
    else:
        print("Needs two arguments <filename> <filesize> in that order.")
        sys.exit(-1)


if __name__ == "__main__":
    main(sys.argv)

