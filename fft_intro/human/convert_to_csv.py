import os
import sys
from pydub import AudioSegment
from typing import List

def m4a_to_csv(src: str, dest: str, prefix: str) -> int:
    m4a_files = [f for f in os.listdir(src)
                 if os.path.isfile(os.path.join(src, f)) and
                 os.path.splitext(f)[1] == ".m4a"]

    if not os.path.exists(dest):
        os.makedirs(dest)
        
    nfiles = 0
    for m4a in m4a_files:
        data = AudioSegment.from_file(os.path.join(src, m4a))._data
        numbers = []
        for i in range(len(data)//2):
            numbers.append(int.from_bytes(data[i*2:i*2 + 2],
                                          "little", signed=True))

        ofilename = f"{dest}/{prefix}_{nfiles}.csv"
        with open(ofilename, 'w') as fpw:
            for n in numbers:
                fpw.write(f"{n}\n")

        fpw.close()
        nfiles += 1

    return nfiles


def main(argv: List[str]) -> None:
    if (len(argv) == 4):
        m4a_to_csv(src=argv[1], dest=argv[2], prefix=argv[3])
        sys.exit(0)
    else:
        print("The program takes four arguments.")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
